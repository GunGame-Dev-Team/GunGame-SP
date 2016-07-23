# ../gungame/plugins/included/gg_turbo/configuration.py

"""Creates the gg_turbo configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame Imports
#   Config
from gungame.core.config.manager import GunGameConfigManager

# Plugin Imports
from .info import info


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('quick_switch',
           )


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:

    with _config.cvar('quick_switch') as quick_switch:
        quick_switch.add_text()
