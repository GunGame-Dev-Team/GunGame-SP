# ../gungame/plugins/included/gg_hostage_objective/configuration.py

"""Creates the gg_hostage_objective configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame Imports
#   Config
from gungame.core.config.manager import GunGameConfigManager

# Plugin Imports
from .info import info


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('killed_count',
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
    with _config.cvar('rescued_levels', 1) as rescued_levels:
        rescued_levels.add_text()

    with _config.cvar('rescued_count', 2) as rescued_count:
        rescued_count.add_text()

    with _config.cvar('rescued_skip_knife') as rescued_skip_knife:
        rescued_skip_knife.add_text()

    with _config.cvar('rescued_skip_nade') as rescued_skip_nade:
        rescued_skip_nade.add_text()

    with _config.cvar('stopped_levels', 1) as stopped_levels:
        stopped_levels.add_text()

    with _config.cvar('stopped_count', 2) as stopped_count:
        stopped_count.add_text()

    with _config.cvar('stopped_skip_knife') as stopped_skip_knife:
        stopped_skip_knife.add_text()

    with _config.cvar('stopped_skip_nade') as stopped_skip_nade:
        stopped_skip_nade.add_text()

    with _config.cvar('killed_levels', 1) as killed_levels:
        killed_levels.add_text()

    with _config.cvar('killed_count', 2) as killed_count:
        killed_count.add_text()
