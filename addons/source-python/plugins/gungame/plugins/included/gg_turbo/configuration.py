# ../gungame/plugins/included/gg_turbo/configuration.py

"""Creates the gg_turbo configuration."""

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
    "multiple_kills",
    "quick_switch",
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with (
    GunGameConfigManager(info.name) as _config,
    _config.cvar(
        name="quick_switch",
    ) as quick_switch,
    _config.cvar(
        name="multiple_kills",
    ) as multiple_kills,
):
    quick_switch.add_text()
    multiple_kills.add_text()
