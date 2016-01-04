# ../gungame/plugins/included/gg_elimination/configuration.py

"""Creates the gg_elimination configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Translations
from translations.strings import LangStrings

# GunGame Imports
#   Config
from gungame.core.config.manager import GunGameConfigManager

# Plugin Imports
from .info import info


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('spawn_joiners',
           )


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_config_strings = LangStrings('gungame/included_plugins/config/gg_elimination')


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:
    with _config.cvar(
            'spawn_joiners', 0,
            _config_strings['Spawn-Joiners']) as spawn_joiners:
        pass
