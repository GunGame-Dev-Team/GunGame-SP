# ../gungame/plugins/included/gg_disable_objectives/configuration.py

"""Creates the gg_disable_objectives configuration."""

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
            'gg_disable_objectives_type', 0, ConVarFlags.NONE,
            'Set to the types of objectives to disable.') as disable_types:
        disable_types.Options.append('1 = Disable Bombing Objectives.')
        disable_types.Options.append('2 = Disable Hostage Objectives.')
        disable_types.Options.append(
            '3 = Disable Bombing AND Hostage Objectives.')
