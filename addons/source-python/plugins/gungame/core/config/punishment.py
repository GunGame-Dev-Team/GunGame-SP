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
    'afk_punish',
    'afk_length',
    'afk_type',
    'level_one_team_kill',
    'retry_punish',
    'suicide_punish',
    'team_kill_punish',
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager('punishment') as _config:
    _config._cvar_prefix = 'gg_'

    # AFK
    # TODO: add in functionality
    with _config.cvar(
        name='afk',
    ) as afk_punish:
        afk_punish.add_text()
    with _config.cvar(
        name='afk_type',
    ) as afk_type:
        afk_type.add_text()
    with _config.cvar(
        name='afk_length',
    ) as afk_length:
        afk_length.add_text()

    # Retry
    # TODO: add in functionality
    with _config.cvar(
        name='retry',
    ) as retry_punish:
        retry_punish.add_text()

    # Suicide
    with _config.cvar(
        name='suicide',
    ) as suicide_punish:
        suicide_punish.add_text()

    # Team-kill
    with _config.cvar(
        name='team_kill',
    ) as team_kill_punish:
        team_kill_punish.add_text()
    with _config.cvar(
        name='level_one_team_kill',
    ) as level_one_team_kill:
        level_one_team_kill.add_text()
