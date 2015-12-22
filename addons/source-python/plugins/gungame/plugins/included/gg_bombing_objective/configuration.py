# ../gungame/plugins/included/gg_bombing_objective/configuration.py

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

# Plugin Imports
from .info import info


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as config:
    with config.cvar(
            'defused_levels', 1, ConVarFlags.NONE,
            'The number of levels to increase for ' +
            'successfully defusing the bomb.') as defused_levels:
        pass

    with config.cvar(
            'defused_skip_knife', 0, ConVarFlags.NONE,
            'Enable/disable skipping knife level by ' +
            'defusing.') as defused_skip_knife:
        pass

    with config.cvar(
            'defused_skip_nade', 0, ConVarFlags.NONE,
            'Enable/disable skipping nade level by ' +
            'defusing.') as defused_skip_nade:
        pass

    with config.cvar(
            'detonated_levels', 1, ConVarFlags.NONE,
            'The number of levels to increase for ' +
            'successfully detonating the bomb.') as detonated_levels:
        pass

    with config.cvar(
            'detonated_skip_knife', 0, ConVarFlags.NONE,
            'Enable/disable skipping knife level by ' +
            'successfully detonating the bomb.') as detonated_skip_knife:
        pass

    with config.cvar(
            'detonated_skip_nade', 0, ConVarFlags.NONE,
            'Enable/disable skipping nade level by ' +
            'successfully detonating the bomb.') as detonated_skip_nade:
        pass
