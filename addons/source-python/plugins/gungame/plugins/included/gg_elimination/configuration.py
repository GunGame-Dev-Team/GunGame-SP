# ../gungame/plugins/included/gg_elimination/configuration.py

"""Creates the gg_elimination configuration."""

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
            'spawn_joiners', 0, ConVarFlags.NONE,
            'Enable/Disable spawning late joining players.') as spawn_joiners:
        pass
