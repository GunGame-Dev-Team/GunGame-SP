# ../gungame/addons/included/deathmatch/deathmatch_config.py

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Path
from path import path

# GunGame Imports
#   Config
from gungame.core.config.manager import GunGameConfigManager
#   Translations
from gungame.core.translations.strings import GunGameLangStrings


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_name = path(__file__).parent.namebase

_strings = GGLangStrings(_name)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(_name) as config:
    with config.get_cvar('gg_deathmatch_respawn_delay') as cvar:
        cvar.default = '2'
        cvar.text = _strings[cvar.name].get_string()
