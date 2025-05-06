# ../gungame/plugins/included/gg_teamplay/configuration.py

"""Creates the gg_teamplay configuration."""

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
    "count_grenade_kills",
    "count_melee_kills",
    "end_on_first_kill",
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with (
    GunGameConfigManager(info.name) as _config,
    _config.cvar(name="end_on_first_kill") as end_on_first_kill,
    _config.cvar(name="count_melee_kills") as count_melee_kills,
    _config.cvar(name="count_grenade_kills") as count_grenade_kills,
):
    end_on_first_kill.add_text()
    count_melee_kills.add_text()
    count_grenade_kills.add_text()
