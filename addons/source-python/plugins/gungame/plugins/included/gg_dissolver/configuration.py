# ../gungame/plugins/included/gg_dissolver/configuration.py

"""Creates the gg_disable_objectives configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Cvars
from cvars.flags import ConVarFlags
#   Entities
from entities.constants import DissolveType

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
            'type', 0, ConVarFlags.NONE,
            'Set to the type of dissolver to use.') as dissolver_type:
        for _name in DissolveType.__members__:
            dissolver_type.Options.append('{0} = {1}'.format(
                getattr(DissolveType, _name).real, _name))
        _num_dissolve_types = len(DissolveType)
        dissolver_type.Options.append(
            '{0} = RANDOM'.format(_num_dissolve_types))
        dissolver_type.Options.append(
            '{0} = REMOVE'.format(_num_dissolve_types + 1))

    with config.cvar(
            'magnitude', 2, ConVarFlags.NONE,
            'Set to the magnitude to use when dissolving') as magnitude:
        pass
