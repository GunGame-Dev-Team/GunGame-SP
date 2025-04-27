# ../gungame/core/listeners.py

"""Event and level listeners and misc helper functions."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import defaultdict
from contextlib import suppress

# Source.Python
from colors import BLUE, RED, WHITE
from cvars import ConVar
from engines.server import queue_command_string
from entities.entity import Entity
from events import Event
from filters.entities import EntityIter
from filters.players import PlayerIter
from listeners import OnLevelInit, OnLevelEnd
from listeners.tick import Delay
from players.teams import teams_by_name
from weapons.manager import weapon_manager

# Site-package
from mutagen import MutagenError

# Custom Package
from idle_manager import OnClientBack, OnClientIdle, is_client_idle

# GunGame
from .config.misc import (
    allow_kills_after_round, cancel_on_fire, dynamic_chat_time, give_armor,
    give_defusers, level_on_protect, send_rules_each_map
)
from .config.punishment import (
    afk_length, afk_punish, afk_type, level_one_team_kill, suicide_punish,
    team_kill_punish
)
from .config.warmup import enabled as warmup_enabled, warmup_weapon
from .config.weapon import (
    order_file, order_randomize, multi_kill_override, prop_physics
)
from .credits import gungame_credits
from .events.included.match import GG_Map_End, GG_Start
from .leaders import leader_manager
from .messages.manager import message_manager
from .players.attributes import AttributePostHook
from .players.database import winners_database
from .players.dictionary import player_dictionary
from .rules.command import send_rules
from .sounds.manager import sound_manager
from .status import GunGameMatchStatus, GunGameRoundStatus, GunGameStatus
from .warmup.manager import warmup_manager
from .weapons.groups import incendiary_weapons, melee_weapons
from .weapons.helpers import remove_idle_weapons
from .weapons.manager import weapon_order_manager


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'start_match',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Create a set to store userids that have already had join messages
_joined_players = set()

# Create a set to store userids that have recently switched teams
_team_changers = set()

_melee_weapon = weapon_manager[
    'knife' if 'knife' in melee_weapons else list(melee_weapons)[0]
].name

_spawning_users = set()
_afk_player_delays = {}
_afk_player_rounds = defaultdict(int)
_spec_team = teams_by_name.get('spec')


# =============================================================================
# >> PLAYER GAME EVENTS
# =============================================================================
@Event('player_spawn')
def _player_spawn(game_event):
    """Give the player their level weapon."""
    # Is GunGame active?
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    # Use try/except to get the player's instance
    player = player_dictionary.get(game_event['userid'])
    if player is None:
        return

    # Verify that the player is on a team
    if player.team_index < 2:
        return

    if not player.level:
        return

    if player.userid in _spawning_users:
        return

    _spawning_users.add(player.userid)
    Delay(
        delay=0,
        callback=_spawning_users.remove,
        args=(player.userid,),
    )

    # Spawn protection
    player.give_spawn_protection()

    # Give the player their new weapon
    player.strip_weapons(
        not_filters={'grenade'},
        remove_incendiary=player.level_weapon in incendiary_weapons,
    )
    player.give_level_weapon()

    # Give CTs defusers, if need be
    if player.team_index == 3 and give_defusers.get_bool():
        player.has_defuser = True

    # Give player armor, if necessary
    armor_type = {1: 'kevlar', 2: 'assaultsuit'}.get(give_armor.get_int())
    if armor_type is not None:
        for entity in EntityIter('game_player_equip'):
            entity.remove()
        equip = Entity.create('game_player_equip')
        equip.add_output(f'{_melee_weapon} 1')
        equip.add_output(
            f'item_{armor_type} 1',
            caller=player,
            activator=player,
        )

    # Skip bots
    if player.is_fake_client():
        player.player_state = 0
        return

    # Send the player their level information
    _send_level_info(player)


@Event('player_death')
def _player_death(game_event):
    """Award the killer with a multi-kill increase or level increase."""
    # Is GunGame active?
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    # Is the round active or should kills after the round count?
    if (
        GunGameStatus.ROUND is GunGameRoundStatus.INACTIVE and
        not allow_kills_after_round.get_int()
    ):
        return

    userid = game_event['userid']
    attacker = game_event['attacker']

    # Was this a suicide?
    if attacker in (userid, 0):
        _punish_suicide(userid)
        return

    victim = player_dictionary[userid]
    killer = player_dictionary[attacker]

    # Was this a team-kill?
    if victim.team_index == killer.team_index:
        _punish_team_kill(killer)
        return

    if killer.in_spawn_protection and not level_on_protect.get_int():
        return

    # Did the killer kill using their level's weapon?
    weapon = game_event['weapon']
    if weapon != 'prop_physics':
        if weapon_manager[weapon].basename != killer.level_weapon:
            return
    elif not prop_physics.get_int():
        return

    # Increase the killer's multi_kill
    killer.multi_kill += 1

    # Does the player need leveled up?
    if killer.multi_kill < killer.level_multi_kill:
        return

    # Level the player up
    killer.increase_level(
        levels=1,
        reason='kill',
        victim=userid,
    )


@Event('player_activate')
def _player_activate(game_event):
    """Add player to leaders and send join message."""
    userid = game_event['userid']

    # Add the player to the leader dictionary
    leader_manager.add_player(userid)

    player = player_dictionary[userid]

    # Is the player a bot?
    if player.is_fake_client():
        return

    # Send the rules menu to the player
    if send_rules_each_map.get_int():
        send_rules(player.index)

    # Is the player just joining the game?
    if userid in _joined_players:
        return

    _joined_players.add(userid)
    player.play_gg_sound('welcome')

    if player.wins:
        message = 'Player:Join:Ranked' if player.rank else 'Player:Join:Wins'
        message_manager.chat_message(message, player=player)
        player.update_time_stamp()

    # Print a message if the joining player is in the credits
    for credit_type in gungame_credits:
        for name in gungame_credits[credit_type]:
            steam_id2 = gungame_credits[credit_type][name]['steam_id2']
            steam_id3 = gungame_credits[credit_type][name]['steam_id3']
            if player.steamid in (steam_id2, steam_id3):
                message_manager.chat_message(
                    'Player:Join:Credits',
                    player=player,
                    credit_type=credit_type,
                )
                return


@Event('player_disconnect')
def _player_disconnect(game_event):
    """Store the disconnecting player's values and remove from dictionary."""
    userid = game_event['userid']
    player_dictionary.safe_remove(userid)
    leader_manager.check_disconnect(userid)
    player = player_dictionary.get(userid)
    if player is not None:
        _remove_index_from_afk_dicts(player.index)


@Event('player_team')
def _player_team(game_event):
    """Track team changes for use with suicide punishment."""
    userid = game_event['userid']
    if userid in _team_changers:
        return
    _team_changers.add(userid)
    Delay(
        delay=0.2,
        callback=_team_changers.remove,
        args=(userid,),
    )


@Event('weapon_fire')
def _weapon_fire(game_event):
    """Remove spawn protection, if necessary."""
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    if not cancel_on_fire.get_int():
        return

    player = player_dictionary[game_event['userid']]
    if not player.in_spawn_protection:
        return

    if cancel_on_fire.get_int():
        player.remove_spawn_protection()


# =============================================================================
# >> ROUND GAME EVENTS
# =============================================================================
@Event('round_start')
def _round_start(game_event):
    """Disable buyzones and set the round status to ACTIVE."""
    GunGameStatus.ROUND = GunGameRoundStatus.ACTIVE
    for entity in EntityIter('func_buyzone'):
        entity.disable()

    remove_idle_weapons()

    if afk_type.get_bool():
        return

    for player in PlayerIter(
        is_filters='alive',
        not_filters=['spec', 'un']
    ):
        index = player.index
        if not is_client_idle(index):
            continue

        _afk_player_rounds[index] += 1
        if _afk_player_rounds[index] >= afk_length.get_int():
            _punish_afk(index)


@Event('round_end')
def _round_end(game_event):
    """Set the round status to INACTIVE since the round ended."""
    GunGameStatus.ROUND = GunGameRoundStatus.INACTIVE


# =============================================================================
# >> MISC GAME EVENTS
# =============================================================================
@Event('server_cvar')
def _server_cvar(game_event):
    """Set the weapon order value if the ConVar is for the weapon order."""
    if GunGameStatus.MATCH is GunGameMatchStatus.UNLOADING:
        return

    # Get the ConVar name and its new value
    cvarname = game_event['cvarname']
    cvarvalue = game_event['cvarvalue']

    # Did the weapon order change?
    if cvarname == order_file.name:
        weapon_order_manager.set_active_weapon_order(cvarvalue)

    # Did the randomize value change?
    elif cvarname == order_randomize.name:
        weapon_order_manager.set_randomize(cvarvalue)

    # Did the multi_kill override value change?
    elif cvarname == multi_kill_override.name:
        weapon_order_manager.print_order()

    # Did the warmup weapon change?
    elif cvarname == warmup_weapon.name:
        warmup_manager.set_warmup_weapon()


# =============================================================================
# >> GUNGAME EVENTS
# =============================================================================
@Event('gg_win')
def _gg_win(game_event):
    """Increase the win total for the winner and end the map."""
    # Set the match status
    GunGameStatus.MATCH = GunGameMatchStatus.POST

    # Get the winner
    winner = player_dictionary[game_event['winner']]

    # Increase the winner's win total if they are not a bot
    if not winner.is_fake_client():
        winner.wins += 1

    # Send the winner messages
    message_manager.chat_message(
        message='Winner:Long',
        index=winner.index,
        winner=winner.name,
    )
    for second in range(4):
        Delay(
            delay=second,
            callback=message_manager.center_message,
            kwargs={
                'message': 'Winner:Short',
                'winner': winner.name,
            },
            cancel_on_level_end=True,
        )
    color = {2: RED, 3: BLUE}.get(winner.team_index, WHITE)
    message_manager.top_message(
        message='Winner:Short',
        color=color,
        winner=winner.name
    )

    # Play the winner sound
    winner_sound = sound_manager.play_sound('winner')

    # Set the dynamic chat time, if needed
    if dynamic_chat_time.get_bool() and winner_sound is not None:
        with suppress(MutagenError):
            ConVar('mp_chattime').set_float(winner_sound.duration)

    # End the match to move to the next map
    entity = Entity.find_or_create('game_end')
    entity.end_game()


@Event('gg_map_end')
def _gg_map_end(game_event):
    """Set the match status to POST after the map has ended."""
    GunGameStatus.MATCH = GunGameMatchStatus.POST


@Event('gg_start')
def _gg_start(game_event):
    """Set the match status to ACTIVE and post the weapon order."""
    # Set the match status
    GunGameStatus.MATCH = GunGameMatchStatus.ACTIVE

    # Post the weapon order
    weapon_order_manager.print_order()


@Event('gg_level_up')
def _gg_level_up(game_event):
    """Increase the player leader level and send level info."""
    userid = game_event['leveler']
    leader_manager.player_level_up(userid)
    _send_level_info(player_dictionary[userid])


@Event('gg_level_down')
def _gg_level_down(game_event):
    """Set the player's level in the leader dictionary."""
    userid = game_event['leveler']
    leader_manager.player_level_down(userid)


# =============================================================================
# >> LEVEL LISTENERS
# =============================================================================
@OnLevelInit
def _level_init(map_name):
    """Set match status to INACTIVE when a new map is started."""
    _afk_player_rounds.clear()
    _afk_player_delays.clear()

    # Is GunGame still loading?
    if GunGameStatus.MATCH is GunGameMatchStatus.LOADING:
        return

    # Set the match status
    GunGameStatus.MATCH = GunGameMatchStatus.INACTIVE

    # Prune the database
    winners_database.prune_database()

    # Start match (or warmup)
    start_match()


@OnLevelEnd
def _level_end():
    """Clear the player dictionary on map change."""
    player_dictionary.clear()
    leader_manager.clear()

    if GunGameStatus.MATCH is not GunGameMatchStatus.POST:
        GG_Map_End().fire()


# =============================================================================
# >> ATTRIBUTE LISTENERS
# =============================================================================
@AttributePostHook('multi_kill')
def _post_multi_kill(player, attribute, new_value, old_value):
    """Send multi_kill info message."""
    # Is the multi_kill being reset to 0?
    if not new_value:
        return

    # Is the player going to level up?
    multi_kill = player.level_multi_kill
    if multi_kill == new_value:
        return

    # Send the multi_kill message
    player.hint_message(
        message='LevelInfo:Current:Kills',
        kills=new_value,
        total=multi_kill,
    )
    player.play_gg_sound('multi_kill')


# =============================================================================
# >> AFK LISTENERS
# =============================================================================
@OnClientIdle
def _client_idle(index):
    """Start tracking afk for punishment."""
    if not afk_type.get_bool():
        return

    _afk_player_delays[index] = Delay(
        delay=afk_length.get_float(),
        callback=_punish_afk,
        args=(index,),
        cancel_on_level_end=True,
    )


@OnClientBack
def _remove_index_from_afk_dicts(index):
    """Remove the player's index from the afk dictionaries."""
    _afk_player_rounds.pop(index, None)
    delay = _afk_player_delays.pop(index, None)
    if delay is not None:
        delay.cancel()


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def start_match(ending_warmup=False):
    """Start the match if not already started or on hold."""
    # Is warmup supposed to happen?
    if not ending_warmup and warmup_enabled.get_bool():
        warmup_manager.start_warmup()
        return

    # Is the match supposed to start?
    if GunGameStatus.MATCH is not GunGameMatchStatus.INACTIVE:
        return

    queue_command_string('mp_restartgame 1')
    GG_Start().fire()


def _send_level_info(player):
    """Send level information to the given player."""
    # Get the player's language
    language = player.language

    # Get the player's current level's multi_kill value
    multi_kill = player.level_multi_kill

    # If the multi_kill value is not 1, add the multi_kill to the message
    kills_text = ''
    if multi_kill > 1:
        kills_text = message_manager['LevelInfo:Current:Kills'].get_string(
            language,
            kills=player.multi_kill,
            total=player.level_multi_kill,
        ) + '\n'

    # Get the current leaders
    leaders = leader_manager.current_leaders

    # Get the leader's level
    leader_level = leader_manager.leader_level

    # Are there no leaders?
    if leaders is None:

        # Add the no leaders text to the message
        leaders_text = message_manager[
            'LevelInfo:Leaders:None'
        ].get_string(language)

    # Is the player the only current leader?
    elif len(leaders) == 1 and player.userid in leaders:

        # Add the current leader text to the message
        leaders_text = message_manager[
            'LevelInfo:Leaders:Current'
        ].get_string(language)

    # Is the player one of multiple current leaders?
    elif len(leaders) > 1 and player.userid in leaders:

        # Add the amongst leaders text to the message
        leaders_text = message_manager[
            'LevelInfo:Leaders:Among'
        ].get_string(language)

    # Is the player not one of the current leaders?
    else:

        # Add the current leader text to the message
        leaders_text = message_manager['LevelInfo:Leaders:Level'].get_string(
            language,
            level=leader_level,
            total=weapon_order_manager.max_levels,
            weapon=weapon_order_manager.active[leader_level].weapon,
        )

    # Send the player's level information message
    player.hint_message(
        message='LevelInfo:Current',
        player=player,
        total=weapon_order_manager.max_levels,
        kills=kills_text,
        leader=leaders_text,
    )


def _punish_suicide(userid):
    """Punish the player for suiciding."""
    levels = suicide_punish.get_int()
    if not levels:
        return

    if userid in _team_changers:
        return

    player = player_dictionary.get(userid)
    if player is None:
        return

    if player.level == 1:
        return

    player.decrease_level(
        levels=levels,
        reason='suicide'
    )
    player.chat_message(
        message='Punishment:Suicide',
        player=player,
    )


def _punish_team_kill(player):
    """Punish the player for team killing."""
    levels = team_kill_punish.get_int()
    if not levels:
        return

    if player.levels == 1:
        if level_one_team_kill.get_int():
            player.slay()
            player.chat_message(
                message='Punishment:TeamKill:Slay',
            )
        return

    player.decrease_level(
        levels=levels,
        reason='team-kill',
    )
    player.chat_message(
        message='Punishment:TeamKill:Level',
        player=player,
    )


def _punish_afk(index):
    """Punish the player for being afk."""
    punishment = afk_punish.get_int()
    if not punishment:
        return

    player = player_dictionary.from_index(index)
    if punishment == 1:
        player.kick(
            message=message_manager['Punishment:AFK:Kick'].get_string(
                language=player.language,
            ),
        )

    else:
        if _spec_team is not None:
            player.team = _spec_team
