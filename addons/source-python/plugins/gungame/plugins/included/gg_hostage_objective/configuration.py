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
with GunGameConfigManager(info.name) as config:
    with config.cvar(
            'gg_hostage_objective_rescued_levels', 1, ConVarFlags.NONE,
            'The number of levels to increase for ' +
            'successfully rescuing hostages.') as cvar:
        ...

    with config.cvar(
            'gg_hostage_objective_rescued_count', 2, ConVarFlags.NONE,
            'The number of rescued hostages required ' +
            'for a level increase.') as cvar:
        ...

    with config.cvar(
            'gg_hostage_objective_rescued_skip_knife', 0, ConVarFlags.NONE,
            'Enable/disable skipping knife level ' +
            'by rescuing hostages.') as cvar:
        ...

    with config.cvar(
            'gg_hostage_objective_rescued_skip_nade', 0, ConVarFlags.NONE,
            'Enable/disable skipping nade level ' +
            'by rescuing hostages.') as cvar:
        ...

    with config.cvar(
            'gg_hostage_objective_stopped_levels', 1, ConVarFlags.NONE,
            'The number of levels to increase for ' +
            'stopping (killing) rescuers.') as cvar:
        ...

    with config.cvar(
            'gg_hostage_objective_rescued_count', 2, ConVarFlags.NONE,
            'The number of stopped (killed) rescuers required ' +
            'for a level increase.') as cvar:
        ...

    with config.cvar(
            'gg_hostage_objective_stopped_skip_knife', 0, ConVarFlags.NONE,
            'Enable/disable skipping knife level by ' +
            'stopping (killing) rescuers.') as cvar:
        ...

    with config.cvar(
            'gg_hostage_objective_stopped_skip_nade', 0, ConVarFlags.NONE,
            'Enable/disable skipping nade level by ' +
            'stopping (killing) rescuers.') as cvar:
        ...

    with config.cvar(
            'gg_hostage_objective_killed_levels', 1, ConVarFlags.NONE,
            'The number of levels to descrease for killing hostages.') as cvar:
        ...

    with config.cvar(
            'gg_hostage_objective_killed_count', 2, ConVarFlags.NONE,
            'The number of hostage kills required ' +
            'for a level decrease.') as cvar:
        ...
