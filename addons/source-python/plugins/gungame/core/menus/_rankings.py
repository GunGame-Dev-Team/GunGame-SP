# ../gungame/core/menus/_rankings.py

"""Provides the menu base for winners and rank."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Menus
from menus import PagedMenu
from menus import PagedOption

# GunGame Imports
#   Menus
from gungame.core.menus import _menu_strings
#   Players
from gungame.core.players.database import winners_database


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def get_winners_menu(player):
    """"""
    menu = PagedMenu(title=_menu_strings['Winners:Title'])
    if not winners_database:
        menu.description = _menu_strings['Winners:None']
        return menu

    winners = sorted(
        winners_database, key=lambda uniqueid: (
            winners_database[uniqueid].wins,
            -winners_database[uniqueid].time_stamp), reverse=True)
    for rank, uniqueid in enumerate(winners, 1):
        instance = winners_database[uniqueid]
        menu.append(PagedOption(
            '{0} - {1} [{2}]'.format(rank, instance.name, instance.wins),
            uniqueid, player.uniqueid == uniqueid, False))
    return menu
