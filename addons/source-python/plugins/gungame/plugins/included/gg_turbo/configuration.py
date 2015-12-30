# ../gungame/plugins/included/gg_turbo/configuration.py

"""Creates the gg_turbo configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Cvars
from cvars.flags import ConVarFlags
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
__all__ = ('quick_switch',
           )


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_config_strings = LangStrings('gungame/included_plugins/config/gg_turbo')


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:

    with _config.cvar(
            'quick_switch', 0,
            _config_strings['Quick-Switch']) as quick_switch:
        pass
