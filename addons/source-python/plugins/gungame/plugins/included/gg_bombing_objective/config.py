# ../gungame/plugins/included/gg_bombing_objective/config.py

"""Creates the gg_bombing_objective configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Cvars
from cvars.flags import ConVarFlags

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
    with config.cvar(
            'gg_bombing_objective_defused_levels', 1, ConVarFlags.NONE,
            'The number of levels to increase for ' +
            'successfully defusing the bomb.') as cvar:
        ...

    with config.cvar(
            'gg_bombing_objective_defused_skip_knife', 0, ConVarFlags.NONE,
            'Enable/disable skipping knife level by defusing.') as cvar:
        ...

    with config.cvar(
            'gg_bombing_objective_defused_skip_nade', 0, ConVarFlags.NONE,
            'Enable/disable skipping nade level by defusing.') as cvar:
        ...

    with config.cvar(
            'gg_bombing_objective_detonated_levels', 1, ConVarFlags.NONE,
            'The number of levels to increase for ' +
            'successfully detonating the bomb.') as cvar:
        ...

    with config.cvar(
            'gg_bombing_objective_detonated_skip_knife', 0, ConVarFlags.NONE,
            'Enable/disable skipping knife level by ' +
            'successfully detonating the bomb.') as cvar:
        ...

    with config.cvar(
            'gg_bombing_objective_detonated_skip_nade', 0, ConVarFlags.NONE,
            'Enable/disable skipping nade level by ' +
            'successfully detonating the bomb.') as cvar:
        ...
