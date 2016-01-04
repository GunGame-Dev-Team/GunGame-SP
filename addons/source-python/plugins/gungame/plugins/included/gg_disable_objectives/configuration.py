# ../gungame/plugins/included/gg_disable_objectives/configuration.py

"""Creates the gg_disable_objectives configuration."""

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
__all__ = ('disable_type',
           )


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_config_strings = LangStrings(
    'gungame/included_plugins/config/gg_disable_objectives')


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:

    with _config.cvar('type', 0, _config_strings['Type']) as disable_type:

        for option in sorted(filter(
                lambda name: name.startswith('Option:'), _config_strings)):

            disable_type.Options.append('{0} = {1}'.format(
                option.split(':')[1], _config_strings[option].get_string()))
