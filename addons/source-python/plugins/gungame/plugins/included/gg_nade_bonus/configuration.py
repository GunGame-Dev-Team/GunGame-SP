# ../gungame/plugins/included/gg_nade_bonus/configuration.py

"""Creates the gg_nade_bonus configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.config.manager import GunGameConfigManager
from gungame.core.weapons.groups import (
    all_grenade_weapons, other_secondary_weapons, pistol_weapons,
    rifle_weapons, shotgun_weapons, smg_weapons,
)

# Plugin
from .info import info


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'bonus_mode',
    'bonus_reset',
    'bonus_weapon',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_single_weapon = (list(other_secondary_weapons) + list(pistol_weapons))[0]
_weapon_list = ','.join([
    (list(smg_weapons) + list(rifle_weapons) + list(shotgun_weapons))[0],
    _single_weapon, list(all_grenade_weapons)[0],
])


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:
    with _config.cvar('weapon') as bonus_weapon:
        bonus_weapon.add_text(
            weapon=_single_weapon,
            weapon_list=_weapon_list,
        )

    with _config.cvar('mode') as bonus_mode:
        bonus_mode.add_text(convar=bonus_weapon.name)

    with _config.cvar('reset') as bonus_reset:
        bonus_reset.add_text(convar=bonus_weapon.name)
