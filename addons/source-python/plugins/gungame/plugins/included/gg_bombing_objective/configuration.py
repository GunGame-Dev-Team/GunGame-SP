# ../gungame/plugins/included/gg_bombing_objective/configuration.py

"""Creates the gg_bombing_objective configuration."""

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
__all__ = ('defused_levels',
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
    with _config.cvar('defused_levels', 1) as defused_levels:
        defused_levels.add_text()

    with _config.cvar('defused_skip_knife') as defused_skip_knife:
        defused_skip_knife.add_text()

    with _config.cvar('defused_skip_nade') as defused_skip_nade:
        defused_skip_nade.add_text()

    with _config.cvar('detonated_levels', 1) as detonated_levels:
        detonated_levels.add_text()

    with _config.cvar('detonated_skip_knife') as detonated_skip_knife:
        detonated_skip_knife.add_text()

    with _config.cvar('detonated_skip_nade') as detonated_skip_nade:
        detonated_skip_nade.add_text()
