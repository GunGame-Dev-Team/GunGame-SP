# ../gungame/plugins/included/gg_quick_weapon/config.py

"""Creates the gg_quick_weapon configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
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
            'gg_quick_weapon_switch', 0,
            description=_strings['gg_quick_weapon_switch']) as cvar:
        cvar.text(_strings[cvar.name + '_text'].get_string())
