# ../gungame/plugins/included/gg_deathmatch/config.py

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
from .info import info


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_strings = GunGameLangStrings(info.name)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as config:
    with config.cvar(
            'gg_deathmatch_respawn_delay', 2,
            description=_strings['gg_deathmatch_respawn_delay']) as cvar:
        cvar.text(_strings[cvar.name + '_text'].get_string())
