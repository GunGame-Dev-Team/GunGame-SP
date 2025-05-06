# ../gungame/plugins/included/gg_hostage_objective/configuration.py

"""Creates the gg_hostage_objective configuration."""

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
    "killed_count",
    "killed_levels",
    "rescued_count",
    "rescued_levels",
    "rescued_skip_knife",
    "rescued_skip_nade",
    "stopped_count",
    "stopped_levels",
    "stopped_skip_knife",
    "stopped_skip_nade",
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with (
    GunGameConfigManager(info.name) as _config,
    _config.cvar(
        name="rescued_levels",
        default=1,
    ) as rescued_levels,
    _config.cvar(
        name="rescued_count",
        default=2,
    ) as rescued_count,
    _config.cvar(name="rescued_skip_knife") as rescued_skip_knife,
    _config.cvar(name="rescued_skip_nade") as rescued_skip_nade,
    _config.cvar(
        name="stopped_levels",
        default=1,
    ) as stopped_levels,
    _config.cvar(
        name="stopped_count",
        default=2,
    ) as stopped_count,
    _config.cvar(name="stopped_skip_knife") as stopped_skip_knife,
    _config.cvar(name="stopped_skip_nade") as stopped_skip_nade,
    _config.cvar(
        name="killed_levels",
        default=1,
    ) as killed_levels,
    _config.cvar(
        name="killed_count",
        default=2,
    ) as killed_count,
):
    rescued_levels.add_text()
    rescued_count.add_text()
    rescued_skip_knife.add_text()
    rescued_skip_nade.add_text()
    stopped_levels.add_text()
    stopped_count.add_text()
    stopped_skip_knife.add_text()
    stopped_skip_nade.add_text()
    killed_levels.add_text()
    killed_count.add_text()
