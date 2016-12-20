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

    with _config.cvar('afk') as afk_punish:
        afk_punish.add_text()
    with _config.cvar('afk_type') as afk_type:
        afk_type.add_text()
    with _config.cvar('afk_length') as afk_length:
        afk_length.add_text()

    with _config.cvar('retry') as retry_punish:
        retry_punish.add_text()

    # Suicide
    with _config.cvar('suicide') as suicide_punish:
        suicide_punish.add_text()

    # Team-kill
    with _config.cvar('team_kill') as team_kill_punish:
        team_kill_punish.add_text()
    with _config.cvar('level_one_team_kill') as level_one_team_kill:
        level_one_team_kill.add_text()
