# ../gungame/listeners.py

"""Event and level listeners and other helper functions."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Contextlib
from contextlib import suppress

# Source.Python Imports
#   Cvars
from cvars import ConVar
#   Entities
from entities.entity import Entity
#   Events
from events import Event
#   Filters
from filters.entities import EntityIter
#   Listeners
from listeners import LevelInit
from listeners import LevelShutdown
from listeners.tick import tick_delays

# GunGame Imports
#   Events
from gungame.core.events.included.match import GG_Start
#   Leaders
from gungame.core.leaders import leader_manager
#   Messages
from gungame.core.messages import message_manager
#   Players
from gungame.core.players.attributes import AttributePostHook
from gungame.core.players.dictionary import player_dictionary
#   Status
from gungame.core.status import GunGameMatchStatus
from gungame.core.status import GunGameStatus
from gungame.core.status import GunGameRoundStatus
#   Warmup
from gungame.core.warmup import warmup_manager
#   Weapons
from gungame.core.weapons.manager import weapon_order_manager


# =============================================================================
# >> PLAYER GAME EVENTS
# =============================================================================
@Event
def player_spawn(game_event):
    """Give the player their level weapon."""
    # Is GunGame active?
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    # Get the userid of the player
    userid = game_event.get_int('userid')

    # Use try/except to get the player's instance
    try:
        player = player_dictionary[userid]
    except ValueError:
        return

    # Verify that the player is on a team
    if player.team < 2:
        return

    # Give player their current weapon
    player.give_level_weapon()

    if player.is_fake_client():
        return

    send_level_info(player)


@Event
def player_death(game_event):
    """Award the killer with a multi-kill increase or level increase."""
    # Is GunGame active?
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    # Is the round active or should kills after the round count?
    if (GunGameStatus.ROUND is GunGameRoundStatus.INACTIVE and
            not ConVar('gg_count_after_round').get_int()):
        return

    # Get the victim
    victim = game_event.get_int('userid')

    # Get the attacker
    attacker = game_event.get_int('attacker')

    # Was this a suicide?
    if attacker in (victim, 0):
        return

    # Get the victim's instance
    vplayer = player_dictionary[victim]

    # Get the attacker's instance
    aplayer = player_dictionary[attacker]

    # Was this a team-kill?
    if vplayer.team == aplayer.team:
        return

    # Did the killer kill using their level's weapon?
    if game_event.get_string('weapon') != aplayer.level_weapon:
        return

    # Increase the killer's multikill
    aplayer.multikill += 1

    # Does the player need leveled up?
    if aplayer.multikill < aplayer.level_multikill:

        # If not, no need to go further
        return

    # Level the player up
    aplayer.increase_level(1, victim, 'kill')


@Event
def player_activate(game_event):
    """Add the player to the leader dictionary."""
    leader_manager.add_player(game_event.get_int('userid'))


@Event
def player_disconnect(game_event):
    """Store the disconnecting player's values and remove from dictionary."""
    player_dictionary.safe_remove(game_event.get_int('userid'))
    leader_manager.check_disconnect(game_event.get_int('userid'))


# =============================================================================
# >> ROUND GAME EVENTS
# =============================================================================
@Event
def round_start(game_event):
    """Disable buyzones and set the round status to ACTIVE."""
    GunGameStatus.ROUND = GunGameRoundStatus.ACTIVE
    for entity in EntityIter('func_buyzone', return_types='entity'):
        entity.disable()


@Event
def round_end(game_event):
    """Set the round status to INACTIVE since the round ended."""
    GunGameStatus.ROUND = GunGameRoundStatus.INACTIVE


# =============================================================================
# >> OTHER GAME EVENTS
# =============================================================================
@Event
def server_cvar(game_event):
    """Set the weapon order value if the ConVar is for the weapon order."""
    cvarname = game_event.get_string('cvarname')
    cvarvalue = game_event.get_string('cvarvalue')
    if cvarname == 'gg_weapon_order_file':
        weapon_order_manager.set_active_weapon_order(cvarvalue)
    elif cvarname == 'gg_weapon_order_randomize':
        weapon_order_manager.set_randomize(cvarvalue)
    elif cvarname == 'gg_multikill_override':
        with suppress(ValueError):
            weapon_order_manager.multikill = int(cvarvalue)
    elif cvarname == 'gg_warmup_weapon':
        warmup_manager.set_warmup_weapon()


# =============================================================================
# >> GUNGAME EVENTS
# =============================================================================
@Event
def gg_win(game_event):
    """Increase the win total for the winner and end the map."""
    GunGameStatus.MATCH = GunGameMatchStatus.POST
    winner = player_dictionary[game_event.get_int('winner')]
    if not winner.is_fake_client():
        winner.wins += 1
    for entity in EntityIter('game_end', return_types='entity'):
        break
    else:
        entity = Entity.create('game_end')
    entity.end_game()
    message_manager.chat_message(
        index=winner.index, message='Player_Won', name=winner.name)
    for second in range(4):
        tick_delays.delay(
            second, message_manager.center_message,
            message='Player_Won_Center', name=winner.name)
    # message_manager.top_message(
    #     message='Player_Won', color=<team_color>, time=4.0, name=winner.name)


@Event
def gg_map_end(game_event):
    """Set the match status to POST after the map has ended."""
    GunGameStatus.MATCH = GunGameMatchStatus.POST


@Event
def gg_start(game_event):
    """Set the match status to ACTIVE when it starts."""
    GunGameStatus.MATCH = GunGameMatchStatus.ACTIVE


@Event
def gg_levelup(game_event):
    """Increase the player leader level and send level info."""
    # Get the player's userid
    userid = game_event.get_int('leveler')

    # Set the player's level in the leader dictionary
    leader_manager.player_levelup(userid)

    # Send the player their new level info
    send_level_info(player_dictionary[userid])


@Event
def gg_leveldown(game_event):
    """Set the player's level in the leader dictionary."""
    leader_manager.player_leveldown(game_event.get_int('leveler'))


# =============================================================================
# >> LEVEL LISTENERS
# =============================================================================
@LevelInit
def level_init(mapname):
    """Set match status to INACTIVE when a new map is started."""
    if GunGameStatus.MATCH is GunGameMatchStatus.LOADING:
        return

    GunGameStatus.MATCH = GunGameMatchStatus.INACTIVE

    # Start match (or warmup)
    start_match()


@LevelShutdown
def level_shutdown():
    """Clear the player dictionary on map change."""
    player_dictionary.clear()


# =============================================================================
# >> ATTRIBUTE LISTENERS
# =============================================================================
@AttributePostHook('multikill')
def post_multikill(player, attribute, new_value, old_value):
    """Send multikill info message."""
    if not new_value:
        return
    multikill = player.level_multikill
    if multikill == new_value:
        return
    player.hint_message(
        message='Multikill_Notification', kills=new_value, total=multikill)


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def start_match():
    """Start the match if not already started or on hold."""
    if ConVar('gg_warmup_round').get_int():
        warmup_manager.start_warmup()
    if GunGameStatus.MATCH is not GunGameMatchStatus.INACTIVE:
        return
    GG_Start().fire()


def send_level_info(player):
    """"""
    language = player.language
    text = message_manager['LevelInfo_Current_Level'].get_string(
        language, level=player.level, total=weapon_order_manager.max_levels)
    text += message_manager['LevelInfo_Current_Weapon'].get_string(
        language, weapon=player.level_weapon)
    multikill = player.level_multikill
    if multikill > 1:
        text += message_manager['LevelInfo_Required_Kills'].get_string(
            language, kills=player.multikill, total=multikill)
    leaders = leader_manager.current_leaders
    leader_level = leader_manager.leader_level
    if leaders is None:
        text += message_manager['LevelInfo_No_Leaders'].get_string(language)
    elif len(leaders) == 1 and player.userid in leaders:
        text += message_manager[
            'LevelInfo_Current_Leader'].get_string(language)
    elif len(leaders) > 1 and player.userid in leaders:
        text += message_manager[
            'LevelInfo_Amongst_Leaders'].get_string(language)
    else:
        text += message_manager['LevelInfo_Leader_Level'].get_string(
            language, level=leader_level,
            total=weapon_order_manager.max_levels,
            weapon=weapon_order_manager.active[leader_level].weapon)

    player.hint_message(message=text)
