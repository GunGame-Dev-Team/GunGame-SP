# ../gungame/plugins/included/gg_hostage_objective/configuration.py

"""Creates the gg_hostage_objective configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Cvars
from cvars.flags import ConVarFlags

# GunGame Imports
#   Config
from gungame.core.config.manager import GunGameConfigManager

# Script Imports
from .info import info


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name, 'gg_hostage_objective_') as config:
    with config.cvar(
            'rescued_levels', 1, ConVarFlags.NONE,
            'The number of levels to increase for ' +
            'successfully rescuing hostages.') as rescued_levels:
        ...

    with config.cvar(
            'rescued_count', 2, ConVarFlags.NONE,
            'The number of rescued hostages required ' +
            'for a level increase.') as rescued_count:
        ...

    with config.cvar(
            'rescued_skip_knife', 0, ConVarFlags.NONE,
            'Enable/disable skipping knife level ' +
            'by rescuing hostages.') as rescued_skip_knife:
        ...

    with config.cvar(
            'rescued_skip_nade', 0, ConVarFlags.NONE,
            'Enable/disable skipping nade level ' +
            'by rescuing hostages.') as rescued_skip_nade:
        ...

    with config.cvar(
            'stopped_levels', 1, ConVarFlags.NONE,
            'The number of levels to increase for ' +
            'stopping (killing) rescuers.') as stopped_levels:
        ...

    with config.cvar(
            'stopped_count', 2, ConVarFlags.NONE,
            'The number of stopped (killed) rescuers required ' +
            'for a level increase.') as stopped_count:
        ...

    with config.cvar(
            'stopped_skip_knife', 0, ConVarFlags.NONE,
            'Enable/disable skipping knife level by ' +
            'stopping (killing) rescuers.') as stopped_skip_knife:
        ...

    with config.cvar(
            'stopped_skip_nade', 0, ConVarFlags.NONE,
            'Enable/disable skipping nade level by ' +
            'stopping (killing) rescuers.') as stopped_skip_nade:
        ...

    with config.cvar(
            'killed_levels', 1, ConVarFlags.NONE,
            'The number of levels to descrease for killing ' +
            'hostages.') as killed_levels:
        ...

    with config.cvar(
            'killed_count', 2, ConVarFlags.NONE,
            'The number of hostage kills required ' +
            'for a level decrease.') as killed_count:
        ...
