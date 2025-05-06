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
    "afk_length",
    "afk_punish",
    "afk_type",
    "level_one_team_kill",
    "suicide_punish",
    "team_kill_punish",
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with (
    GunGameConfigManager("punishment") as _config,
    _config.cvar(name="afk") as afk_punish,
    _config.cvar(name="afk_type") as afk_type,
    _config.cvar(name="afk_length") as afk_length,
    _config.cvar(name="suicide") as suicide_punish,
    _config.cvar(name="team_kill") as team_kill_punish,
    _config.cvar(name="level_one_team_kill") as level_one_team_kill,
):
    # AFK
    afk_punish.add_text()
    afk_type.add_text()
    afk_length.add_text()

    # Suicide
    suicide_punish.add_text()

    # Team-kill
    team_kill_punish.add_text()
    level_one_team_kill.add_text()
