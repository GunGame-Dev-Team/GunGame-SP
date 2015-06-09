# ../gungame/plugins/included/gg_deathmatch/config.py

"""Creates the gg_deathmatch configuration."""

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
    with config.cvar('gg_deathmatch_delay', 2, description=info.translations[
            'gg_deathmatch_delay']) as cvar:
        cvar.text(info.translations[cvar.name + '_text'].get_string())
