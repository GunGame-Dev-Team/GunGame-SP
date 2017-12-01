# ../gungame/core/menus/_rankings.py

"""Provides the menu base for winners and rank."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from menus import PagedMenu

# GunGame
from . import menu_strings
from ._options import ListOption
from ..players.database import winners_database


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'get_winners_menu',
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def get_winners_menu(player):
    """Return a sorted menu of all winners."""
    menu = PagedMenu(title=menu_strings['Winners:Title'])
    if not winners_database:
        menu.description = menu_strings['Winners:None']
        return menu

    winners = sorted(
        winners_database,
        key=lambda key: (
            winners_database[key].wins,
            -winners_database[key].time_stamp,
        ),
        reverse=True,
    )
    for rank, unique_id in enumerate(winners, 1):
        instance = winners_database[unique_id]
        menu.append(
            ListOption(
                choice_index=rank,
                text=f'{instance.name} [{instance.wins}]',
                value=unique_id,
                highlight=player.uniqueid == unique_id,
                selectable=False,
            )
        )
    return menu
