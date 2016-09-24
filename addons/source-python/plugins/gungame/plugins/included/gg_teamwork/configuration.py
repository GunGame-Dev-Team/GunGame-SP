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
    'join_team_level',
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:
    with _config.cvar('join_team_level', 0) as join_team_level:
        join_team_level.add_text()
