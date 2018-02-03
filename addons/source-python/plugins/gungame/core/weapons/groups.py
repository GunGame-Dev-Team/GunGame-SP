# ../gungame/core/weapons/groups.py

"""Create weapon sets by common tags."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import OrderedDict

# Source.Python
from core import GAME_NAME
from filters.weapons import WeaponClassIter


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'all_grenade_weapons',
    'all_primary_weapons',
    'all_secondary_weapons',
    'all_weapons',
    'explosive_weapons',
    'grenade_weapons',
    'incendiary_weapons',
    'individual_weapons',
    'machine_gun_weapons',
    'melee_weapons',
    'other_primary_weapons',
    'other_secondary_weapons',
    'other_weapons',
    'pistol_weapons',
    'rifle_weapons',
    'shotgun_weapons',
    'smg_weapons',
    'sniper_weapons',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
all_weapons = set()
all_primary_weapons = set()
all_secondary_weapons = set()
all_grenade_weapons = set()

_weapon_sets = OrderedDict()

# Primary Weapon sets
shotgun_weapons = _weapon_sets['shotgun'] = set()
smg_weapons = _weapon_sets['smg'] = set()
sniper_weapons = _weapon_sets['sniper'] = set()
rifle_weapons = _weapon_sets['rifle'] = set()
machine_gun_weapons = _weapon_sets['machinegun'] = set()
other_primary_weapons = _weapon_sets['primary'] = set()

# Secondary Weapon sets
pistol_weapons = _weapon_sets['pistol'] = set()
other_secondary_weapons = _weapon_sets['secondary'] = set()

# Projectile Weapon sets
explosive_weapons = _weapon_sets['explosive'] = set()
incendiary_weapons = _weapon_sets['incendiary'] = set()
grenade_weapons = _weapon_sets['grenade'] = set()

# Melee Weapon sets
melee_weapons = _weapon_sets['melee'] = set()

# Other Weapon sets
other_weapons = set()

# Individual Fire Weapon sets
individual_weapons = set()


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _get_weapon_sets():
    for weapon in WeaponClassIter():
        if (
            'objective' in weapon.tags or
            'tool' in weapon.tags or
            'earned' in weapon.tags
        ):
            continue
        if 'all' in weapon.tags and len(weapon.tags) == 1:
            continue
        for tag, weapon_set in _weapon_sets.items():
            if tag in weapon.tags:
                weapon_set.add(weapon.basename)
                break
        else:
            other_weapons.add(weapon.basename)
        if 'primary' in weapon.tags:
            all_primary_weapons.add(weapon.basename)
        if 'secondary' in weapon.tags:
            all_secondary_weapons.add(weapon.basename)
        if 'grenade' in weapon.tags:
            all_grenade_weapons.add(weapon.basename)
        all_weapons.add(weapon.basename)

_get_weapon_sets()

if not all_weapons:
    raise NotImplementedError(
        f'Game {GAME_NAME} not supported, no weapon data.'
    )

# Set the individual fire weapon sets
individual_weapons.update(all_grenade_weapons)
