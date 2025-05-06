# ../gungame/plugins/included/gg_elimination/configuration.py

"""Creates the gg_elimination configuration."""

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
    "spawn_joiners",
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with (
    GunGameConfigManager(info.name) as _config,
    _config.cvar(name="spawn_joiners") as spawn_joiners,
):
    spawn_joiners.add_text()
