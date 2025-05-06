# ../gungame/plugins/included/gg_nade_bonus/configuration.py

"""Creates the gg_nade_bonus configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from enum import IntEnum

# Source.Python
from cvars.flags import ConVarFlags

# GunGame
from gungame.core.config.manager import GunGameConfigManager
from gungame.core.weapons.groups import (
    all_grenade_weapons,
    all_primary_weapons,
    all_secondary_weapons,
)

# Plugin
from .info import info

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "BonusMode",
    "bonus_mode",
    "bonus_reset",
    "bonus_weapon",
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_single_weapon = sorted(all_secondary_weapons)[0]
_weapon_list = ",".join([
    sorted(all_primary_weapons)[0],
    _single_weapon,
    sorted(all_grenade_weapons)[0],
])


# =============================================================================
# >> ENUM CLASSES
# =============================================================================
class BonusMode(IntEnum):
    """Nade bonus mode options."""

    KEEP_LAST_WEAPON = 0
    RESTART_LIST = 1
    LEVEL_PLAYER_UP = 2


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with (
    GunGameConfigManager(info.name) as _config,
    _config.cvar(
        name="weapon",
        default=_single_weapon,
        flags=ConVarFlags.NOTIFY,
    ) as bonus_weapon,
    _config.cvar(
        name="mode",
    ) as bonus_mode,
    _config.cvar(
        name="reset",
    ) as bonus_reset,
):
    bonus_weapon.add_text(
        weapon=_single_weapon,
        weapon_list=_weapon_list,
    )
    bonus_mode.add_text(convar=bonus_weapon.name)
    bonus_reset.add_text(convar=bonus_weapon.name)
