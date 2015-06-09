# ../gungame/plugins/included/gg_quick_weapon/config.py

"""Creates the gg_quick_weapon configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame Imports
#   Config
from gungame.core.config.manager import GunGameConfigManager
#   Plugins
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
            'gg_quick_weapon_switch', 0,
            description=info.translations['gg_quick_weapon_switch']) as cvar:
        cvar.text(info.translations[cvar.name + '_text'].get_string())
