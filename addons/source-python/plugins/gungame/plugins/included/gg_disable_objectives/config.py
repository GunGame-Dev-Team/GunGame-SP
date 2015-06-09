# ../gungame/plugins/included/gg_disable_objectives/config.py

"""Creates the gg_disable_objectives configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame Imports
#   Config
from gungame.core.config.manager import GunGameConfigManager
#   Translations
from gungame.core.plugins.strings import PluginStrings

# Script Imports
from .info import info


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
info.translations = PluginStrings(info.name)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as config:
    with config.cvar(
            info.name, 0, description=info.translations[info.name]) as cvar:
        cvar.text(info.translations[cvar.name + '_text'].get_string())
