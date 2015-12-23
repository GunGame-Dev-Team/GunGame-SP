# ../gungame/core/listeners.py

"""Event and level listeners and other helper functions."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Contextlib
from contextlib import suppress

# Source.Python Imports
#   Colors
from colors import BLUE
from colors import RED
from colors import WHITE
#   Cvars
from cvars import ConVar
#   Entities
from entities.entity import Entity
#   Events
from events import Event
#   Filters
from filters.entities import EntityIter
#   Listeners
from listeners import OnLevelInit
from listeners import OnLevelShutdown
from listeners.tick import tick_delays

# GunGame Imports
#   Config
from gungame.core.config.core.warmup import enabled as warmup_enabled
from gungame.core.config.core.warmup import weapon as warmup_weapon
from gungame.core.config.core.weapons import order_file
from gungame.core.config.core.weapons import order_randomize
from gungame.core.config.core.weapons import multikill_override
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
# >> GLOBAL VARIABLES
# =============================================================================
# Create a set to store userids that have already had join messages
_joined_players = set()


# =============================================================================
# >> PLAYER GAME EVENTS
# =============================================================================
@Event('player_spawn')
def player_spawn(game_event):
    """Give the player their level weapon."""
    # Is GunGame active?
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    # Get the userid of the player
    userid = game_event['userid']

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

    # Skip bots
    if player.is_fake_client():
        return

    # Send the player their level information
    send_level_info(player)


@Event('player_death')
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
    victim = game_event['userid']

    # Get the attacker
    attacker = game_event['attacker']

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
    if game_event['weapon'] != aplayer.level_weapon:
        return

    # Increase the killer's multikill
    aplayer.multikill += 1

    # Does the player need leveled up?
    if aplayer.multikill < aplayer.level_multikill:

        # If not, no need to go further
        return

    # Level the player up
    aplayer.increase_level(1, victim, 'kill')


@Event('player_activate')
def player_activate(game_event):
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

    # Get the message to use
    message = 'JoinPlayer_Ranked' if player.wins else 'JoinPlayer_Rank'

    # Send the joining message
    message_manager.chat_message(message, player=player)

    # TODO: add credits.db to get the following values from
    '''
    # Is the player in the credits?
    if player.steamid in <credits>:
        message_manager.chat_message(
            'JoinPlayer_Credits', name=player.name,
            credit_type=<credits>[player.steamid])
    '''


@Event('player_disconnect')
def player_disconnect(game_event):
    """Store the disconnecting player's values and remove from dictionary."""
    userid = game_event['userid']
    player_dictionary.safe_remove(userid)
    leader_manager.check_disconnect(userid)


# =============================================================================
# >> ROUND GAME EVENTS
# =============================================================================
@Event('round_start')
def round_start(game_event):
    """Disable buyzones and set the round status to ACTIVE."""
    GunGameStatus.ROUND = GunGameRoundStatus.ACTIVE
    for entity in EntityIter('func_buyzone'):
        entity.disable()


@Event('round_end')
def round_end(game_event):
    """Set the round status to INACTIVE since the round ended."""
    GunGameStatus.ROUND = GunGameRoundStatus.INACTIVE


# =============================================================================
# >> OTHER GAME EVENTS
# =============================================================================
@Event('server_cvar')
def server_cvar(game_event):
    """Set the weapon order value if the ConVar is for the weapon order."""
    # Get the ConVar name and its new value
    cvarname = game_event['cvarname']
    cvarvalue = game_event['cvarvalue']

    # Did the weapon order change?
    if cvarname == order_file.get_name():

        # Set the new weapon order
        weapon_order_manager.set_active_weapon_order(cvarvalue)

    # Did the randomize value change?
    elif cvarname == order_randomize.get_name():

        # Set the randomize value
        weapon_order_manager.set_randomize(cvarvalue)

    # Did the multikill override value change?
    elif cvarname == multikill_override.get_name():

        # Set the new multikill override value
        with suppress(ValueError):
            weapon_order_manager.multikill = int(cvarvalue)

    # Did the warmup weapon change?
    elif cvarname == warmup_weapon.get_name():

        # Set the new warmup weapon
        warmup_manager.set_warmup_weapon()


# =============================================================================
# >> GUNGAME EVENTS
# =============================================================================
@Event('gg_win')
def gg_win(game_event):
    """Increase the win total for the winner and end the map."""
    # Set the match status
    GunGameStatus.MATCH = GunGameMatchStatus.POST

    # Get the winner
    winner = player_dictionary[game_event['winner']]

    # Increase the winner's win total if they are not a bot
    if not winner.is_fake_client():
        winner.wins += 1

    # Get a game_end entity
    entity = Entity.find_or_create('game_end')

    # End the match to move to the next map
    entity.end_game()

    # Send the winner messages
    message_manager.chat_message(
        index=winner.index, message='Winner_Player', name=winner.name)
    for second in range(4):
        tick_delays.delay(
            second, message_manager.center_message,
            message='Winner_Player_Center', name=winner.name)
    color = {2: RED, 3: BLUE}.get(winner.team, WHITE)
    message_manager.top_message('Player_Won', color, 4.0, name=winner.name)


@Event('gg_map_end')
def gg_map_end(game_event):
    """Set the match status to POST after the map has ended."""
    GunGameStatus.MATCH = GunGameMatchStatus.POST


@Event('gg_start')
def gg_start(game_event):
    """Set the match status to ACTIVE and post the weapon order."""
    # Set the match status
    GunGameStatus.MATCH = GunGameMatchStatus.ACTIVE

    # Post the weapon order
    weapon_order_manager.print_order()


@Event('gg_levelup')
def gg_levelup(game_event):
    """Increase the player leader level and send level info."""
    # Get the player's userid
    userid = game_event['leveler']

    # Set the player's level in the leader dictionary
    leader_manager.player_levelup(userid)

    # Send the player their new level info
    send_level_info(player_dictionary[userid])


@Event('gg_leveldown')
def gg_leveldown(game_event):
    """Set the player's level in the leader dictionary."""
    leader_manager.player_leveldown(game_event['leveler'])


# =============================================================================
# >> LEVEL LISTENERS
# =============================================================================
@OnLevelInit
def level_init(map_name):
    """Set match status to INACTIVE when a new map is started."""
    # Is GunGame still loading?
    if GunGameStatus.MATCH is GunGameMatchStatus.LOADING:
        return

    # Set the match status
    GunGameStatus.MATCH = GunGameMatchStatus.INACTIVE

    # Start match (or warmup)
    start_match()


@OnLevelShutdown
def level_shutdown():
    """Clear the player dictionary on map change."""
    player_dictionary.clear()


# =============================================================================
# >> ATTRIBUTE LISTENERS
# =============================================================================
@AttributePostHook('multikill')
def post_multikill(player, attribute, new_value, old_value):
    """Send multikill info message."""
    # Is the multikill being reset to 0?
    if not new_value:
        return

    # Is the player going to level up?
    multikill = player.level_multikill
    if multikill == new_value:
        return

    # Send the multikill message
    player.hint_message(
        message='Multikill_Notification', kills=new_value, total=multikill)


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


def send_level_info(player):
    """Send level information to the given player."""
    # Get the player's language
    language = player.language

    # Get the player's current level information
    text = message_manager['LevelInfo_Current_Level'].get_string(
        language, player=player, total=weapon_order_manager.max_levels)

    # Add the player's weapon information to the message
    text += message_manager['LevelInfo_Current_Weapon'].get_string(
        language, player=player)

    # Get the player's current level's multikill value
    multikill = player.level_multikill

    # If the multikill value is not 1, add the multikill to the message
    if multikill > 1:
        text += message_manager['LevelInfo_Required_Kills'].get_string(
            language, player=player)

    # Get the current leaders
    leaders = leader_manager.current_leaders

    # Get the leader's level
    leader_level = leader_manager.leader_level

    # Are there no leaders?
    if leaders is None:

        # Add the no leaders text to the message
        text += message_manager['LevelInfo_No_Leaders'].get_string(language)

    # Is the player the only current leader?
    elif len(leaders) == 1 and player.userid in leaders:

        # Add the current leader text to the message
        text += message_manager[
            'LevelInfo_Current_Leader'].get_string(language)

    # Is the player one of multiple current leaders?
    elif len(leaders) > 1 and player.userid in leaders:

        # Add the amongst leaders text to the message
        text += message_manager[
            'LevelInfo_Amongst_Leaders'].get_string(language)

    # Is the player not one of the current leaders?
    else:

        # Add the current leader text to the message
        text += message_manager['LevelInfo_Leader_Level'].get_string(
            language, level=leader_level,
            total=weapon_order_manager.max_levels,
            weapon=weapon_order_manager.active[leader_level].weapon)

    # Send the player's level information message
    player.hint_message(message=text)
