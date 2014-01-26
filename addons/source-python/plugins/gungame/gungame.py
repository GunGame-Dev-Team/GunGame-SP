from cvars import ServerVar
from events import Event
from gungame.core.events.storage import GGResourceList


def load():

    # Initialize GunGame logging

    # Initialize GunGame translations

    # Initialize GunGame commands

    # Initialize GunGame menus

    # Initialize GunGame weapon orders

    # Initialize GunGame events
    GGResourceList.load_events()

    # Initialize GunGame sounds

    # Initialize GunGame database

    # Initialize GunGame configs

    # Set gungame public variables

    # Add gungame to sv_tags


def unload():
    # Remove gungame from sv_tags
    # Remove flags from public variables
    # Clean GunGame configs
    # Clean GunGame players
    # Clean GunGame database
    # Clean GunGame sounds
    # Clean GunGame events
    # Clean GunGame weapon orders
    # Clean GunGame menus
    # Clean GunGame translations
    # Clean GunGame logging


@Event
def player_spawn(game_event):
    ''''''

    # 
    if not GunGameStatus.Match:

        # 
        return

    # 
    userid = game_event.get_int('userid')

    # 
    try:

        # 
        player = PlayerDictionary[userid]

    # 
    except ValueError:

        # 
        return

    # Verify that the user is on a team
    if player.team < 2:

        # 
        return

    # Give player their current weapon
    player.give_current_weapon()


@Event
def player_death(game_event):
    if not GunGameStatus.Match:
        return
    if not GunGameStatus.Round and not gg_count_after_round.get_int():
        return
    victim = game_event.get_int('userid')
    attacker = game_event.get_int('attacker')
    if attacker in (victim, 0):
        return
    vplayer = PlayerDictionary[victim]
    aplayer = PlayerDictionary[attacker]
    if vplayer.team == aplayer.team:
        return
    if aplayer.multikill >= get_level_multikill(aplayer.level):
        if aplayer.level == get_max_levels():
            # Player wins!!!
            return
        aplayer.level += 1
        aplayer.multikill = 0
        return
    aplayer.multikill += 1
