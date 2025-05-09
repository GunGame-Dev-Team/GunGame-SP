# ../gungame/plugins/included/gg_nade_bonus/configuration.py

"""Creates the gg_nade_bonus configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.config.manager import GunGameConfigManager
from gungame.core.weapons.groups import all_secondary_weapons

# Plugin
from .info import info

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "bonus_weapon",
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_single_weapon = sorted(all_secondary_weapons)[0]


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with (
    GunGameConfigManager(info.name) as _config,
    _config.cvar(
        name="weapon",
        default=_single_weapon,
    ) as bonus_weapon,
):
    bonus_weapon.add_text()
