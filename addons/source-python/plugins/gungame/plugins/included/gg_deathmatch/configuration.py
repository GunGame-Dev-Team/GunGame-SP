# ../gungame/plugins/included/gg_deathmatch/configuration.py

"""Creates the gg_deathmatch configuration."""

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
    'delay',
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:
    with _config.cvar(
        name='delay',
        default=2,
    ) as delay:
        delay.add_text()
