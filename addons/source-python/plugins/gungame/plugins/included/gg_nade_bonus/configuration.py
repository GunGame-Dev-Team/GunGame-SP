# ../gungame/plugins/included/gg_nade_bonus/configuration.py

"""Creates the gg_nade_bonus configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from cvars.flags import ConVarFlags

# GunGame
from gungame.core.config.manager import GunGameConfigManager
from gungame.core.weapons.groups import (
    all_grenade_weapons, all_primary_weapons, all_secondary_weapons,
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
_single_weapon = sorted(all_secondary_weapons)[0]
_weapon_list = ','.join([
    sorted(all_primary_weapons)[0],
    _single_weapon,
    sorted(all_grenade_weapons)[0],
])


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:
    with _config.cvar(
        name='weapon',
        default=_single_weapon,
        flags=ConVarFlags.NOTIFY,
    ) as bonus_weapon:
        bonus_weapon.add_text(
            weapon=_single_weapon,
            weapon_list=_weapon_list,
        )

    with _config.cvar('mode') as bonus_mode:
        bonus_mode.add_text(convar=bonus_weapon.name)

    with _config.cvar('reset') as bonus_reset:
        bonus_reset.add_text(convar=bonus_weapon.name)
