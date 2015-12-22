# ../gungame/core/config/core/weapons.py

"""GunGame weapons configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Cvars
from cvars.flags import ConVarFlags

# GunGame Imports
#   Config
from gungame.core.config.manager import GunGameConfigManager


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager('weapon') as config:
    with config.cvar(
            'order_file', 'default_weapon_order', ConVarFlags.NOTIFY,
            'The weapon order file to use for GunGame.') as cvar:
        ...
