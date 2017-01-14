# ../gungame/plugins/included/gg_nade_bonus/configuration.py

"""Creates the gg_nade_bonus configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.config.manager import GunGameConfigManager

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
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:
    with _config.cvar('weapon') as bonus_weapon:
        bonus_weapon.add_text()

    with _config.cvar('mode') as bonus_mode:
        bonus_mode.add_text()

    with _config.cvar('reset') as bonus_reset:
        bonus_reset.add_text()
