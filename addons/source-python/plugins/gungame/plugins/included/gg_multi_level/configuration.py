# ../gungame/plugins/included/gg_multi_level/configuration.py

"""Creates the gg_deathmatch configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.config.manager import GunGameConfigManager

# Plugin
from .info import info

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "gravity",
    "levels",
    "speed",
    "tk_attacker_reset",
    "tk_victim_reset",
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with (
    GunGameConfigManager(info.name) as _config,
    _config.cvar(
        name="levels",
        default=3,
    ) as levels,
    _config.cvar(
        name="speed",
        default=150,
    ) as speed,
    _config.cvar(
        name="gravity",
        default=100,
    ) as gravity,
    _config.cvar(name="tk_attacker_reset") as tk_attacker_reset,
    _config.cvar(name="tk_victim_reset") as tk_victim_reset,
):
    levels.add_text()
    speed.add_text()
    gravity.add_text()
    tk_attacker_reset.add_text()
    tk_victim_reset.add_text()
