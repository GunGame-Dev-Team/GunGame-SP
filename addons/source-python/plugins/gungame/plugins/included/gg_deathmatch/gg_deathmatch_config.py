# ../gungame/plugins/included/gg_deathmatch/gg_deathmatch_config.py

"""Creates the gg_deathmatch configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Site-Package Imports
#   Path
from path import Path

# GunGame Imports
#   Config
from gungame.core.config.manager import GunGameConfigManager
#   Translations
from gungame.core.translations.strings import GunGameLangStrings


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_name = Path(__file__).parent.namebase

_strings = GunGameLangStrings(_name)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(_name) as config:
    delay = config.get_cvar('gg_deathmatch_respawn_delay')
    delay.default = '2'
    delay.text = _strings[delay.name].get_string()
