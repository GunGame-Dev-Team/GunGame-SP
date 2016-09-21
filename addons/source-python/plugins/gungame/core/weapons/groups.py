# ../gungame/core/weapons/groups.py

"""Create weapon sets by common tags."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from core import GAME_NAME
from filters.weapons import WeaponClassIter


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'all_weapons',
    'explosive_weapons',
    'grenade_weapons',
    'incendiary_weapons',
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

# Primary Weapon sets
shotgun_weapons = set()
smg_weapons = set()
sniper_weapons = set()
rifle_weapons = set()
machine_gun_weapons = set()
other_primary_weapons = set()

# Secondary Weapon sets
pistol_weapons = set()
other_secondary_weapons = set()

# Projectile Weapon sets
explosive_weapons = set()
incendiary_weapons = set()
grenade_weapons = set()

# Melee Weapon sets
melee_weapons = set()

# Other Weapon sets
other_weapons = set()


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _get_weapon_sets():
    for weapon in WeaponClassIter():
        if 'objective' in weapon.tags or 'tool' in weapon.tags:
            continue
        if 'all' in weapon.tags and len(weapon.tags) == 1:
            continue
        if 'shotgun' in weapon.tags:
            shotgun_weapons.add(weapon.basename)
        elif 'smg' in weapon.tags:
            smg_weapons.add(weapon.basename)
        elif 'sniper' in weapon.tags:
            sniper_weapons.add(weapon.basename)
        elif 'rifle' in weapon.tags:
            rifle_weapons.add(weapon.basename)
        elif 'machinegun' in weapon.tags:
            machine_gun_weapons.add(weapon.basename)
        elif 'primary' in weapon.tags:
            other_primary_weapons.add(weapon.basename)
        elif 'pistol' in weapon.tags:
            pistol_weapons.add(weapon.basename)
        elif 'secondary' in weapon.tags:
            other_secondary_weapons.add(weapon.basename)
        elif 'explosive' in weapon.tags:
            explosive_weapons.add(weapon.basename)
        elif 'incendiary' in weapon.tags:
            incendiary_weapons.add(weapon.basename)
        elif 'grenade' in weapon.tags:
            grenade_weapons.add(weapon.basename)
        elif 'melee' in weapon.tags:
            melee_weapons.add(weapon.basename)
        else:
            other_weapons.add(weapon.basename)
        all_weapons.add(weapon.basename)

_get_weapon_sets()

if not len(all_weapons):
    raise NotImplementedError(
        'Game {game} not supported, no weapon data.'.format(game=GAME_NAME)
    )
