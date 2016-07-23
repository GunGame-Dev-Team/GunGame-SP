# ../gungame/core/menus/score.py

"""Score menu functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Menus
from menus import PagedMenu
#   Players
from players.entity import Player

# GunGame Imports
#   Menus
from . import _menu_strings
from ._options import ListOption
#   Players
from ..players.dictionary import player_dictionary
#   Plugins
from ..plugins.manager import gg_plugin_manager
#   Status
from ..status import GunGameMatchStatus
from ..status import GunGameStatus


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def send_score_menu(index):
    """Send the score menu to the player."""
    menu = PagedMenu(title=_menu_strings['Score:Title'])
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        menu.append(_menu_strings['Inactive'])
    elif 'gg_teamplay' in gg_plugin_manager:
        # TODO: Implement teamplay menus once teamplay is implemented
        pass
    else:
        player = Player(index)
        for userid in sorted(
                player_dictionary,
                key=lambda userid: player_dictionary[userid].level,
                reverse=True):
            current_player = player_dictionary[userid]
            menu.append(ListOption(
                current_player.level, current_player.name,
                current_player.unique_id,
                current_player.unique_id == player.unique_id, False))
    menu.send(index)
