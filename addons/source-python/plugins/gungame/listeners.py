# ../gungame/listeners.py

"""Event and level listeners."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from cvars import ConVar
from entities.entity import Entity
from events import Event
from filters.entities import EntityIter
from listeners import LevelShutdown

from gungame.core.players.dictionary import player_dictionary
from gungame.core.status import GunGameStatus
from gungame.core.status import gungame_status


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event
def player_spawn(game_event):
    """Give the player their level weapon."""
    # Is GunGame active?
    if gungame_status.match is not GunGameStatus.ACTIVE:
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

    from messages import SayText2
    SayText2(message='{0} - {1}/{2}'.format(
        player.level, player.multikill, player.level_multikill)).send(
            player.index)


@Event
def player_death(game_event):
    """Award the killer with a multi-kill increase or level increase."""
    # Is GunGame active?
    if gungame_status.match is not GunGameStatus.ACTIVE:
        return

    # Is the round active or should kills after the round count?
    if (gungame_status.round is GunGameStatus.INACTIVE and
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
def player_disconnect(game_event):
    """Store the disconnecting player's values and remove from dictionary."""
    player_dictionary.safe_remove(game_event.get_int('userid'))


@Event
def round_start(game_event):
    """Disable buyzones."""
    for entity in EntityIter('func_buyzone', return_types='entity'):
        entity.disable()


# =============================================================================
# >> GUNGAME EVENTS
# =============================================================================
@Event
def gg_win(game_event):
    """Increase the win total for the winner and end the map."""
    winner = player_dictionary[game_event.get_int('winner')]
    if not winner.is_fake_client():
        winner.wins += 1
    for entity in EntityIter('game_end', return_types='entity'):
        break
    else:
        entity = Entity.create('game_end')
    entity.end_game()


# =============================================================================
# >> LISTENERS
# =============================================================================
@LevelShutdown
def level_shutdown():
    """Clear the player dictionary on map change."""
    player_dictionary.clear()
