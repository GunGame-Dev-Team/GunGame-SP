# ../gungame/gungame.py

""""""

from cvars.tags import sv_tags
from events import Event
from filters.entities import EntityIter
from listeners import LevelShutdown

from gungame.info import info
from gungame.core.config.manager import config_manager
from gungame.core.events.storage import gg_resource_list
from gungame.core.players.dictionary import player_dictionary
from gungame.core.status import gungame_status
from gungame.core.weapons.manager import weapon_order_manager


def load():
    """Initialize GunGame."""
    # Initialize GunGame logging

    # Initialize GunGame translations

    # Initialize GunGame commands

    # Initialize GunGame menus

    # Initialize GunGame weapon orders
    weapon_order_manager.get_weapon_orders()

    # Initialize GunGame events
    gg_resource_list.load_events()

    # Initialize GunGame sounds

    # Initialize GunGame database

    # Initialize GunGame configs
    config_manager.load_configs()

    # Set the starting weapon convars
    weapon_order_manager.set_start_convars()

    # Add gungame to sv_tags
    sv_tags.add(info.basename)


def unload():
    """Clean up GunGame."""
    # Remove gungame from sv_tags
    sv_tags.remove(info.basename)

    # Clean GunGame configs
    # Clean GunGame players
    # Clean GunGame database
    # Clean GunGame sounds
    # Clean GunGame events
    # Clean GunGame weapon orders
    # Clean GunGame menus
    # Clean GunGame translations
    # Clean GunGame logging

    # Re-enable buyzones
    for entity in EntityIter('func_buyzone', return_types='entity'):
        entity.enable()


@Event
def player_spawn(game_event):
    """Give the player their weapon."""
    # Is GunGame active?
    if not gungame_status.match:
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
    """Award the killer if necessary."""
    # Is GunGame active?
    if not gungame_status.match:
        return

    # Is the round active or should kills after the round count?
    if not gungame_status.round and not gg_count_after_round.get_int():
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

    # Does the player need leveled up?
    if aplayer.multikill >= aplayer.level_multikill -1:

        print('leveling up')

        # Was this a winning kill?
        if aplayer.level == weapon_order_manager.active.max_levels:
            print('YOU WON!!')
            # Player wins!!!
            return

        # Increase the killer's level
        aplayer.level += 1

        # Reset the killer's multikill
        aplayer.multikill = 0

        print('LEVEL', aplayer.level)

        # No need to go further
        return

    print('increase multikill')
    # Increase the killer's multikill
    aplayer.multikill += 1


@Event
def player_disconnect(game_event):
    player_dictionary.safe_remove(game_event.get_int('userid'))


@Event
def round_start(game_event):
    for entity in EntityIter('func_buyzone', return_types='entity'):
        entity.disable()


@LevelShutdown
def level_shutdown():
    player_dictionary.clear()
