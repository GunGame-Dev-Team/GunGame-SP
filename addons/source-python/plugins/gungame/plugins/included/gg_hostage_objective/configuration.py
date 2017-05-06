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
    'killed_count',
    'killed_levels',
    'rescued_count',
    'rescued_levels',
    'rescued_skip_knife',
    'rescued_skip_nade',
    'stopped_count',
    'stopped_levels',
    'stopped_skip_knife',
    'stopped_skip_nade',
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:

    with _config.cvar(
        name='rescued_levels',
        default=1,
    ) as rescued_levels:
        rescued_levels.add_text()

    with _config.cvar(
        name='rescued_count',
        default=2,
    ) as rescued_count:
        rescued_count.add_text()

    with _config.cvar(
        name='rescued_skip_knife',
    ) as rescued_skip_knife:
        rescued_skip_knife.add_text()

    with _config.cvar(
        name='rescued_skip_nade',
    ) as rescued_skip_nade:
        rescued_skip_nade.add_text()

    with _config.cvar(
        name='stopped_levels',
        default=1,
    ) as stopped_levels:
        stopped_levels.add_text()

    with _config.cvar(
        name='stopped_count',
        default=2,
    ) as stopped_count:
        stopped_count.add_text()

    with _config.cvar(
        name='stopped_skip_knife',
    ) as stopped_skip_knife:
        stopped_skip_knife.add_text()

    with _config.cvar(
        name='stopped_skip_nade',
    ) as stopped_skip_nade:
        stopped_skip_nade.add_text()

    with _config.cvar(
        name='killed_levels',
        default=1,
    ) as killed_levels:
        killed_levels.add_text()

    with _config.cvar(
        name='killed_count',
        default=2,
    ) as killed_count:
        killed_count.add_text()
