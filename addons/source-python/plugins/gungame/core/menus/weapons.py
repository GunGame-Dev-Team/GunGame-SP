# ../gungame/core/menus/weapons.py

"""Weapon menu functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from menus import PagedMenu

# GunGame
from . import menu_strings
from ._options import ListOption
from ..commands.registration import register_command_callback
from ..players.dictionary import player_dictionary
from ..status import GunGameMatchStatus, GunGameStatus
from ..weapons.manager import weapon_order_manager


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'send_weapons_menu',
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
@register_command_callback('weapons', 'Weapons:Text')
def send_weapons_menu(index):
    """Send the weapon menu to the player."""
    menu = PagedMenu(title=menu_strings['Weapons:Title'])
    if GunGameStatus.MATCH is GunGameMatchStatus.WARMUP:
        menu.append(menu_strings['Warmup'])
    elif GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        menu.append(menu_strings['Inactive'])
    else:
        player = player_dictionary.from_index(index)
        for level, instance in weapon_order_manager.active.items():
            menu.append(
                ListOption(
                    choice_index=level,
                    text='{weapon} [{multi_kill}]'.format(
                        weapon=instance.weapon,
                        multi_kill=instance.multi_kill,
                    ),
                    value=level,
                    highlight=level == player.level,
                    selectable=False,
                )
            )
    menu.send(index)
