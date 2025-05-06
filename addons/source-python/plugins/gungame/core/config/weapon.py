# ../gungame/core/config/weapon.py

"""GunGame weapons configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from cvars.flags import ConVarFlags

# GunGame
from ..config.manager import GunGameConfigManager

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "multi_kill_override",
    "order_file",
    "order_randomize",
    "prop_physics",
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with (
    GunGameConfigManager("weapon") as _config,
    _config.cvar(
        name="order_file",
        default="default",
        flags=ConVarFlags.NOTIFY,
    ) as order_file,
    _config.cvar(
        name="order_randomize",
        flags=ConVarFlags.NOTIFY,
    ) as order_randomize,
    _config.cvar(
        name="multi_kill_override",
        flags=ConVarFlags.NOTIFY,
    ) as multi_kill_override,
    _config.cvar(
        name="prop_physics",
    ) as prop_physics,
):
    order_file.add_text()
    order_randomize.add_text()
    multi_kill_override.add_text()
    prop_physics.add_text()
