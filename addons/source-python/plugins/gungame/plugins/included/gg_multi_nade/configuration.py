# ../gungame/plugins/included/gg_multi_nade/configuration.py

"""Creates the gg_multi_nade configuration."""

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
    'max_nades',
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:
    with _config.cvar('max_nades', 0) as max_nades:
        max_nades.add_text()
