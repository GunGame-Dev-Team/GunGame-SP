# ../gungame/core/menus/score.py

"""Score menu functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from menus import PagedMenu
from players.entity import Player

# GunGame
from . import menu_strings
from ._options import ListOption
from ..players.dictionary import player_dictionary
from ..plugins.manager import gg_plugin_manager
from ..status import GunGameMatchStatus, GunGameStatus


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'send_score_menu',
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def send_score_menu(index):
    """Send the score menu to the player."""
    menu = PagedMenu(title=menu_strings['Score:Title'])
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        menu.append(menu_strings['Inactive'])
    elif gg_plugin_manager.is_team_game:
        # TODO: Implement team menus once teamplay/teamwork are implemented
        pass
    else:
        player = Player(index)
        for userid in sorted(
            player_dictionary,
            key=lambda key: player_dictionary[key].level,
            reverse=True,
        ):
            current_player = player_dictionary[userid]
            menu.append(
                ListOption(
                    current_player.level,
                    current_player.name,
                    current_player.unique_id,
                    current_player.unique_id == player.unique_id,
                    False,
                )
            )
    menu.send(index)
