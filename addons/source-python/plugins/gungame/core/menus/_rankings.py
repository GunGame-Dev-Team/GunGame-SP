# ../gungame/core/menus/_rankings.py

"""Provides the menu base for winners and rank."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Menus
from menus import PagedMenu

# GunGame Imports
#   Menus
from gungame.core.menus import _menu_strings
from gungame.core.menus._options import ListOption
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
        menu.append(ListOption(
            rank, '{0} [{1}]'.format(instance.name, instance.wins),
            uniqueid, player.uniqueid == uniqueid, False))
    return menu
