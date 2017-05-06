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
    'multiple_kills',
    'quick_switch',
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:

    with _config.cvar(
        name='quick_switch',
    ) as quick_switch:
        quick_switch.add_text()

    with _config.cvar(
        name='multiple_kills',
    ) as multiple_kills:
        multiple_kills.add_text()
