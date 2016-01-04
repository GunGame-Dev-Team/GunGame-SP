# ../gungame/plugins/included/gg_hostage_objective/configuration.py

"""Creates the gg_hostage_objective configuration."""

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
__all__ = ('killed_count',
           'killed_levels',
           'rescued_count',
           'rescued_levels',
           'rescued_skip_knife',
           'rescued_skip_nade',
           'stopped_count',
           'stopped_levels',
           'stopped_skip_knife',
           'stopped_skip_nade',
           )


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_config_strings = LangStrings(
    'gungame/included_plugins/config/gg_hostage_objective')


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:
    with _config.cvar(
            'rescued_levels', 1,
            _config_strings['Rescued-Levels']) as rescued_levels:
        pass

    with _config.cvar(
            'rescued_count', 2,
            _config_strings['Rescued-Count']) as rescued_count:
        pass

    with _config.cvar(
            'rescued_skip_knife', 0,
            _config_strings['Rescued-Skip-Knife']) as rescued_skip_knife:
        pass

    with _config.cvar(
            'rescued_skip_nade', 0,
            _config_strings['Rescued-Skip-Nade']) as rescued_skip_nade:
        pass

    with _config.cvar(
            'stopped_levels', 1,
            _config_strings['Stopped-Levels']) as stopped_levels:
        pass

    with _config.cvar(
            'stopped_count', 2,
            _config_strings['Stopped-Count']) as stopped_count:
        pass

    with _config.cvar(
            'stopped_skip_knife', 0,
            _config_strings['Stopped-Skip-Knife']) as stopped_skip_knife:
        pass

    with _config.cvar(
            'stopped_skip_nade', 0,
            _config_strings['Stopped-Skip-Nade']) as stopped_skip_nade:
        pass

    with _config.cvar(
            'killed_levels', 1,
            _config_strings['Killed-Levels']) as killed_levels:
        pass

    with _config.cvar(
            'killed_count', 2,
            _config_strings['Killed-Count']) as killed_count:
        pass
