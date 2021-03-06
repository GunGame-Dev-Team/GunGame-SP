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
    'defused_levels',
    'defused_skip_knife',
    'defused_skip_nade',
    'detonated_levels',
    'detonated_skip_knife',
    'detonated_skip_nade',
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:
    with _config.cvar(
        name='defused_levels',
        default=1,
    ) as defused_levels:
        defused_levels.add_text()

    with _config.cvar(
        name='defused_skip_knife',
    ) as defused_skip_knife:
        defused_skip_knife.add_text()

    with _config.cvar(
        name='defused_skip_nade',
    ) as defused_skip_nade:
        defused_skip_nade.add_text()

    with _config.cvar(
        name='detonated_levels',
        default=1,
    ) as detonated_levels:
        detonated_levels.add_text()

    with _config.cvar(
        name='detonated_skip_knife',
    ) as detonated_skip_knife:
        detonated_skip_knife.add_text()

    with _config.cvar(
        name='detonated_skip_nade',
    ) as detonated_skip_nade:
        detonated_skip_nade.add_text()
