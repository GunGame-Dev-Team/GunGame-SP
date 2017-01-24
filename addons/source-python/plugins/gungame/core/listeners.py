# ../gungame/core/listeners.py

"""Event and level listeners and misc helper functions."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from contextlib import suppress

# Source.Python
from colors import BLUE, RED, WHITE
from cvars import ConVar
from entities.entity import Entity
from events import Event
from filters.entities import EntityIter
from listeners import OnLevelInit, OnLevelEnd
from listeners.tick import Delay
from weapons.manager import weapon_manager

# Site-package
from mutagen import MutagenError

# GunGame
from .config.misc import (
    allow_kills_after_round, cancel_on_fire, dynamic_chat_time, give_armor,
    give_defusers, level_on_protect,
)
from .config.punishment import (
    level_one_team_kill, suicide_punish, team_kill_punish,
)
from .config.warmup import enabled as warmup_enabled, weapon as warmup_weapon
from .config.weapon import (
    order_file, order_randomize, multi_kill_override, prop_physics
)
from .credits import gungame_credits
from .events.included.match import GG_Start
from .leaders import leader_manager
from .messages import message_manager
from .players.attributes import AttributePostHook
from .players.dictionary import player_dictionary
from .sounds.manager import sound_manager
from .status import GunGameMatchStatus, GunGameRoundStatus, GunGameStatus
from .warmup import warmup_manager
from .weapons.groups import melee_weapons
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
    'knife' if 'knife' in melee_weapons else melee_weapons[0]
].name


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
    try:
        player = player_dictionary[game_event['userid']]
    except ValueError:
        return

    # Verify that the player is on a team
    if player.team < 2:
        return

    # Spawn protection
    player.give_spawn_protection()

    # Give the player their new weapon
    player.strip_weapons()
    player.give_level_weapon()

    # Give CTs defusers, if need be
    if player.team == 3 and give_defusers.get_bool():
        player.has_defuser = True

    # Give player armor, if necessary
    armor_type = {1: 'kevlar', 2: 'assaultsuit'}.get(give_armor.get_int())
    if armor_type is not None:
        equip = Entity.find_or_create('game_player_equip')
        equip.add_output('{weapon} 1'.format(weapon=_melee_weapon))
        equip.add_output(
            'item_{armor_type} 1'.format(
                armor_type=armor_type
            ),
            caller=player,
            activator=player,
        )

    # Skip bots
    if player.is_fake_client():
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

    # Get the victim
    userid = game_event['userid']

    # Get the attacker
    attacker = game_event['attacker']

    # Was this a suicide?
    if attacker in (userid, 0):
        _punish_suicide(userid)
        return

    # Get the victim's instance
    victim = player_dictionary[userid]

    # Get the attacker's instance
    killer = player_dictionary[attacker]

    # Was this a team-kill?
    if victim.team == killer.team:
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

        # If not, no need to go further
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
    # Get the player's userid
    userid = game_event['userid']

    # Add the player to the leader dictionary
    leader_manager.add_player(userid)

    # Is the player just joining the game?
    if userid in _joined_players:
        return

    # Add the userid to the joined players set
    _joined_players.add(userid)

    # Get the player's instance
    player = player_dictionary[userid]

    # Is the player a bot?
    if player.is_fake_client():
        return

    if player.wins:
        message = 'Player:Join:Ranked' if player.rank else 'Player:Join:Wins'
        message_manager.chat_message(message, player=player)

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


@Event('player_team')
def _player_team(game_event):
    userid = game_event['userid']
    if userid in _team_changers:
        return
    _team_changers.add(userid)
    Delay(0.2, _team_changers.remove, (userid, ))


@Event('weapon_fire')
def _weapon_fire(game_event):
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
    if GunGameStatus.MATCH == GunGameMatchStatus.UNLOADING:
        return

    # Get the ConVar name and its new value
    cvarname = game_event['cvarname']
    cvarvalue = game_event['cvarvalue']

    # Did the weapon order change?
    if cvarname == order_file.name:

        # Set the new weapon order
        weapon_order_manager.set_active_weapon_order(cvarvalue)

    # Did the randomize value change?
    elif cvarname == order_randomize.name:

        # Set the randomize value
        weapon_order_manager.set_randomize(cvarvalue)

    # Did the multi_kill override value change?
    elif cvarname == multi_kill_override.name:

        # Print out the new weapon order
        weapon_order_manager.print_order()

    # Did the warmup weapon change?
    elif cvarname == warmup_weapon.name:

        # Set the new warmup weapon
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
            second,
            message_manager.center_message,
            kwargs={
                'message': 'Winner:Short',
                'winner': winner.name,
            }
        )
    color = {2: RED, 3: BLUE}.get(winner.team, WHITE)
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
    # Is GunGame still loading?
    if GunGameStatus.MATCH is GunGameMatchStatus.LOADING:
        return

    # Set the match status
    GunGameStatus.MATCH = GunGameMatchStatus.INACTIVE

    # Start match (or warmup)
    start_match()


@OnLevelEnd
def _level_end():
    """Clear the player dictionary on map change."""
    player_dictionary.clear()


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
    player.play_sound('multi_kill')


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def start_match():
    """Start the match if not already started or on hold."""
    # Is warmup supposed to happen?
    if warmup_enabled.get_int():

        # Start warmup
        warmup_manager.start_warmup()
        return

    # Is the match supposed to start?
    if GunGameStatus.MATCH is GunGameMatchStatus.INACTIVE:

        # Start the match
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
