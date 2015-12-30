# ../gungame/plugins/included/gg_bombing_objective/configuration.py

"""Creates the gg_bombing_objective configuration."""

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
__all__ = ('defused_levels',
           'defused_skip_knife',
           'defused_skip_nade',
           'detonated_levels',
           'detonated_skip_knife',
           'detonated_skip_nade',
           )


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_config_strings = LangStrings(
    'gungame/included_plugins/config/gg_bombing_objective')


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:
    with _config.cvar(
            'defused_levels', 1,
            _config_strings['Defused-Levels']) as defused_levels:
        pass

    with _config.cvar(
            'defused_skip_knife', 0,
            _config_strings['Defused-Skip-Knife']) as defused_skip_knife:
        pass

    with _config.cvar(
            'defused_skip_nade', 0,
            _config_strings['Defused-Skip-Nade']) as defused_skip_nade:
        pass

    with _config.cvar(
            'detonated_levels', 1,
            _config_strings['Detonated-Levels']) as detonated_levels:
        pass

    with _config.cvar(
            'detonated_skip_knife', 0,
            _config_strings['Detonated-Skip-Knife']) as detonated_skip_knife:
        pass

    with _config.cvar(
            'detonated_skip_nade', 0,
            _config_strings['Detonated-Skip-Nade']) as detonated_skip_nade:
        pass
