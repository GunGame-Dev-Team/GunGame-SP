# ../gungame/core/config/punishment.py

"""GunGame punishment configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from .manager import GunGameConfigManager


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'suicide_punish',
    'team_kill_punish',
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager('punishment') as _config:
    _config._cvar_prefix = 'gg_'

    # TODO: AFK

    # TODO: Retry

    # Suicide
    with _config.cvar('suicide') as suicide_punish:
        suicide_punish.add_text()

    # Team-kill
    with _config.cvar('team_kill') as team_kill_punish:
        team_kill_punish.add_text()
    with _config.cvar('level_one_team_kill') as level_one_team_kill:
        level_one_team_kill.add_text()
