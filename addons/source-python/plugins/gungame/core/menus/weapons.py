# ../gungame/core/menus/weapons.py

"""Weapon menu functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Menus
from menus import PagedMenu
#   Players
from players.helpers import userid_from_index

# GunGame Imports
#   Menus
from . import _menu_strings
from ._options import ListOption
#   Players
from ..players.dictionary import player_dictionary
#   Status
from ..status import GunGameMatchStatus
from ..status import GunGameStatus
#   Weapons
from ..weapons.manager import weapon_order_manager


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def send_weapons_menu(index):
    """Send the weapon menu to the player."""
    menu = PagedMenu(title=_menu_strings['Weapons:Title'])
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        menu.append(_menu_strings['Inactive'])
    else:
        player = player_dictionary[userid_from_index(index)]
        for level, instance in weapon_order_manager.active.items():
            menu.append(ListOption(
                level, '{0} [{1}]'.format(instance.weapon, instance.multi_kill),
                level, level == player.level, False))
    menu.send(index)
