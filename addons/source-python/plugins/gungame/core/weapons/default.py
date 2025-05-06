# ../gungame/core/weapons/default.py

"""Create default weapon orders."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import OrderedDict
from itertools import chain
from random import randint, shuffle

# Source.Python
from translations.strings import LangStrings

# GunGame
from .groups import (
    all_primary_weapons,
    all_secondary_weapons,
    all_weapons,
    explosive_weapons,
    grenade_weapons,
    incendiary_weapons,
    machine_gun_weapons,
    melee_weapons,
    other_primary_weapons,
    other_secondary_weapons,
    other_weapons,
    pistol_weapons,
    rifle_weapons,
    shotgun_weapons,
    smg_weapons,
    sniper_weapons,
)
from ..config.weapon import order_randomize
from ..paths import GUNGAME_WEAPON_ORDER_PATH

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "create_default_weapon_orders",
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_weapon_strings = LangStrings("gungame/weapon_order")

_weapon_groups = OrderedDict([
    ("PISTOLS", sorted(pistol_weapons)),
    ("OTHER SECONDARY WEAPONS", sorted(other_secondary_weapons)),
    ("SMGS", sorted(smg_weapons)),
    ("SHOTGUNS", sorted(shotgun_weapons)),
    ("RIFLES", sorted(rifle_weapons)),
    ("SNIPER RIFLES", sorted(sniper_weapons)),
    ("MACHINE GUNS", sorted(machine_gun_weapons)),
    ("OTHER PRIMARY WEAPONS", sorted(other_primary_weapons)),
    ("OTHER WEAPONS", sorted(other_weapons)),
    ("EXPLOSIVES", sorted(explosive_weapons)),
    ("INCENDIARIES", sorted(incendiary_weapons)),
    ("GRENADES", sorted(grenade_weapons)),
    ("MELEE", sorted(melee_weapons)),
])


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def create_default_weapon_orders():
    """Create all default weapon orders."""
    _create_default_order()
    _create_short_order()
    _create_random_order()
    _create_nade_bonus_order()


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _create_default_order():
    """Create the default weapon order file, if necessary."""
    default_order = GUNGAME_WEAPON_ORDER_PATH / "default.txt"
    if default_order.is_file():
        return
    default_weapons = [
        weapon for weapon in chain.from_iterable(_weapon_groups.values())
        if weapon not in grenade_weapons
    ]
    weapons = "\n".join(default_weapons)
    with default_order.open("w") as open_file:
        open_file.write(_default_header)
        open_file.write(f"{weapons}\n")


def _create_short_order():
    """Create the short weapon order file, if necessary."""
    short_order = GUNGAME_WEAPON_ORDER_PATH / "short.txt"
    if short_order.is_file():
        return
    with short_order.open("w") as open_file:
        open_file.write(_default_header)
        for weapon in sorted(pistol_weapons) + sorted(other_secondary_weapons):
            open_file.write(f"{weapon}\n")


def _create_random_order():
    """Create the random weapon order file, if necessary."""
    random_order = GUNGAME_WEAPON_ORDER_PATH / "random.txt"
    if random_order.is_file():
        return
    shuffle_weapons = [
        weapon for weapon in all_weapons if weapon not in grenade_weapons
    ]
    shuffle(shuffle_weapons)
    with random_order.open("w") as open_file:
        open_file.write(_default_header)
        for weapon in shuffle_weapons:
            multi_kill = randint(0, 3)
            if not multi_kill:
                continue
            if multi_kill == 1:
                open_file.write(f"{weapon}\n")
            else:
                open_file.write(f"{weapon} {multi_kill}\n")


def _create_nade_bonus_order():
    """Create the nade bonus weapon order file, if necessary."""
    nade_bonus = GUNGAME_WEAPON_ORDER_PATH / "nade_bonus.txt"
    if nade_bonus.is_file():
        return
    weapon_copy = sorted(all_secondary_weapons)
    if not weapon_copy:
        weapon_copy = sorted(all_primary_weapons)
    with nade_bonus.open("w") as open_file:
        open_file.write(_default_header)
        for weapon in weapon_copy:
            open_file.write(f"{weapon} 2\n")


def _get_header():
    longest = max(map(len, all_weapons)) + 2
    header = "// " + "\n// ".join(
        _weapon_strings["default"].get_string(
            order_randomize=order_randomize.get_string(),
        ).splitlines(),
    )
    for group, weapons in _weapon_groups.items():
        if not weapons:
            continue
        header += f"\n\n// {group}:\n// "
        header += "\n// ".join([
            f'  {one.ljust(longest)}{two.ljust(longest) if two else ""}{three}'
            for one, two, three in _split_group(weapons)
        ])

    return header + "\n\n"


def _split_group(group):
    for index in range(0, len(group), 3):
        current = group[index:index + 3]
        if len(current) != 3:  # noqa: PLR2004
            current += [""] * (3 - len(current))
        yield current


_default_header = _get_header()
