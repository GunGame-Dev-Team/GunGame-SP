# ../gungame/plugins/included/gg_quick_weapon/config.py

"""Creates the gg_quick_weapon configuration."""

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
            'gg_quick_weapon_switch', 0, ConVarFlags.NONE,
            'Enable/disable allowing players to immediately use ' +
            'their new weapon upon receiving it.') as cvar:
        ...
