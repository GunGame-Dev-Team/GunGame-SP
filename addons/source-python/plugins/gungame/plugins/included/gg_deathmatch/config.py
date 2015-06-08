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

# Script Imports
from gg_deathmatch.info import info


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_strings = GunGameLangStrings(info.name)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as config:
    with config.cvar('gg_deathmatch_respawn_delay', 2) as delay:
        delay.text = _strings[delay.name].get_string()
