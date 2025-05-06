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
    "send_weapons_menu",
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
@register_command_callback("weapons", "Weapons:Text")
def send_weapons_menu(index):
    """Send the weapon menu to the player."""
    menu = PagedMenu(title=menu_strings["Weapons:Title"])
    if GunGameStatus.MATCH is GunGameMatchStatus.WARMUP:
        menu.append(menu_strings["Warmup"])
    elif GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        menu.append(menu_strings["Inactive"])
    else:
        player = player_dictionary.from_index(index)
        for level, instance in weapon_order_manager.active.items():
            menu.append(
                ListOption(
                    choice_index=level,
                    text=f"{instance.weapon} [{instance.multi_kill}]",
                    value=level,
                    highlight=level == player.level,
                    selectable=False,
                ),
            )

        page_index = get_level_page(menu=menu, level=player.level)
        menu.set_player_page(player_index=index, page_index=page_index)
    menu.send(index)


def get_level_page(menu, level):
    """Return the page of the player's current level."""
    for n in range(menu.last_page_index + 1):
        if level in [
            item.choice_index for item in menu._get_options(n)  # noqa: SLF001
        ]:
            return n

    return None
