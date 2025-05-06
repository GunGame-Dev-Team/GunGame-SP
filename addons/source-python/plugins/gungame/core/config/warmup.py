# ../gungame/core/config/warmup.py

"""GunGame warmup configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from cvars.flags import ConVarFlags

# GunGame
from .manager import GunGameConfigManager

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "enabled",
    "max_extensions",
    "min_players",
    "players_reached",
    "warmup_time",
    "warmup_weapon",
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with (
    GunGameConfigManager("warmup") as _config,
    _config.cvar(name="enabled") as enabled,
    _config.cvar(
        name="weapon",
        default="hegrenade",
        flags=ConVarFlags.NOTIFY,
    ) as warmup_weapon,
    _config.cvar(
        name="time",
        default=30,
    ) as warmup_time,
    _config.cvar(
        name="min_players",
        default=4,
    ) as min_players,
    _config.cvar(
        name="max_extensions",
        default=1,
    ) as max_extensions,
    _config.cvar(
        name="players_reached",
    ) as players_reached,
):
    enabled.add_text()
    warmup_weapon.add_text()
    warmup_time.add_text()
    min_players.add_text()
    max_extensions.add_text()
    players_reached.add_text()
