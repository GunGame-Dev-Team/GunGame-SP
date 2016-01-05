# ../gungame/core/menus/leaders.py

"""Leader menu functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Menus
from menus import SimpleMenu
#   Players
from players.entity import Player

# GunGame Imports
#   Leaders
from gungame.core.leaders import leader_manager
#   Menus
from gungame.core.menus import _menu_strings
#   Players
from gungame.core.players.dictionary import player_dictionary
#   Plugins
from gungame.core.plugins.manager import gg_plugin_manager
#   Status
from gungame.core.status import GunGameMatchStatus
from gungame.core.status import GunGameStatus
#   Weapons
from gungame.core.weapons.manager import weapon_order_manager


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def send_leaders_menu(index):
    """Send the leaders menu to the player."""
    menu = SimpleMenu()
    menu.append(_menu_strings['Leader:Current'])
    language = Player(index).language
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        menu.append(_menu_strings['Inactive'])
    elif 'gg_teamplay' in gg_plugin_manager:
        # TODO: Implement teamplay menus once teamplay is implemented
        menu.clear()
        menu.append(_menu_strings['Leader:TeamPlay'])
    elif leader_manager.current_leaders is None:
        menu.append(_menu_strings['Leader:None'])
    else:
        level = leader_manager.leader_level
        menu.append(_menu_strings['Leader:Level'].get_string(
            language, level=level,
            weapon=weapon_order_manager.active[level].weapon))
        for userid in leader_manager.current_leaders:
            menu.append('* {0}'.format(player_dictionary[userid].name))
    menu.send(index)
