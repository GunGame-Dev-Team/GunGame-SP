# ../gungame/plugins/included/gg_bombing_objective/configuration.py

"""Creates the gg_bombing_objective configuration."""

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
    "defused_levels",
    "defused_skip_knife",
    "defused_skip_nade",
    "detonated_levels",
    "detonated_skip_knife",
    "detonated_skip_nade",
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with (
    GunGameConfigManager(info.name) as _config,
    _config.cvar(
        name="defused_levels",
        default=1,
    ) as defused_levels,
    _config.cvar(name="defused_skip_knife") as defused_skip_knife,
    _config.cvar(name="defused_skip_nade") as defused_skip_nade,
    _config.cvar(
        name="detonated_levels",
        default=1,
    ) as detonated_levels,
    _config.cvar(name="detonated_skip_knife") as detonated_skip_knife,
    _config.cvar(name="detonated_skip_nade") as detonated_skip_nade,
):
    defused_levels.add_text()
    defused_skip_knife.add_text()
    defused_skip_nade.add_text()
    detonated_levels.add_text()
    detonated_skip_knife.add_text()
    detonated_skip_nade.add_text()
