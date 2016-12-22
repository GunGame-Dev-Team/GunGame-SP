# ../gungame/core/menus/leaders.py

"""Leader menu functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from menus import PagedMenu
from players.entity import Player

# GunGame
from ..leaders import leader_manager
from . import menu_strings
from ._options import StarOption
from ..players.dictionary import player_dictionary
from ..plugins.manager import gg_plugin_manager
from ..status import GunGameMatchStatus, GunGameStatus
from ..weapons.manager import weapon_order_manager


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'send_leaders_menu',
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def send_leaders_menu(index):
    """Send the leaders menu to the player."""
    menu = PagedMenu(title=menu_strings['Leader:Current'])
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        menu.append(menu_strings['Inactive'])
    elif gg_plugin_manager.is_team_game:
        # TODO: Implement team menus once teamplay/teamwork are implemented
        menu.append(menu_strings['Leader:Team'])
    elif leader_manager.current_leaders is None:
        menu.append(menu_strings['Leader:None'])
    else:
        level = leader_manager.leader_level
        menu.description = menu_strings['Leader:Level'].get_string(
            Player(index).language,
            level=level,
            weapon=weapon_order_manager.active[level].weapon,
        )
        for userid in leader_manager.current_leaders:
            menu.append(StarOption(player_dictionary[userid].name))
    menu.send(index)
