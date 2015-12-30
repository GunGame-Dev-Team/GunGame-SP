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
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:
    with _config.cvar(
            'rescued_levels', 1,
            'The number of levels to increase for ' +
            'successfully rescuing hostages.') as rescued_levels:
        pass

    with _config.cvar(
            'rescued_count', 2,
            'The number of rescued hostages required ' +
            'for a level increase.') as rescued_count:
        pass

    with _config.cvar(
            'rescued_skip_knife', 0,
            'Enable/disable skipping knife level ' +
            'by rescuing hostages.') as rescued_skip_knife:
        pass

    with _config.cvar(
            'rescued_skip_nade', 0,
            'Enable/disable skipping nade level ' +
            'by rescuing hostages.') as rescued_skip_nade:
        pass

    with _config.cvar(
            'stopped_levels', 1,
            'The number of levels to increase for ' +
            'stopping (killing) rescuers.') as stopped_levels:
        pass

    with _config.cvar(
            'stopped_count', 2,
            'The number of stopped (killed) rescuers required ' +
            'for a level increase.') as stopped_count:
        pass

    with _config.cvar(
            'stopped_skip_knife', 0,
            'Enable/disable skipping knife level by ' +
            'stopping (killing) rescuers.') as stopped_skip_knife:
        pass

    with _config.cvar(
            'stopped_skip_nade', 0,
            'Enable/disable skipping nade level by ' +
            'stopping (killing) rescuers.') as stopped_skip_nade:
        pass

    with _config.cvar(
            'killed_levels', 1,
            'The number of levels to descrease for killing ' +
            'hostages.') as killed_levels:
        pass

    with _config.cvar(
            'killed_count', 2,
            'The number of hostage kills required ' +
            'for a level decrease.') as killed_count:
        pass
