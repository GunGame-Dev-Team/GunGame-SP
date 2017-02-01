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
    'enabled',
    'max_extensions',
    'min_players',
    'players_reached',
    'warmup_time',
    'warmup_weapon',
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager('warmup') as _config:
    with _config.cvar('enabled') as enabled:
        enabled.add_text()

    with _config.cvar(
        'weapon', 'hegrenade', flags=ConVarFlags.NOTIFY,
    ) as warmup_weapon:
        warmup_weapon.add_text()

    with _config.cvar('time', 30) as warmup_time:
        warmup_time.add_text()

    with _config.cvar('min_players', 4) as min_players:
        min_players.add_text()

    with _config.cvar('max_extensions', 1) as max_extensions:
        max_extensions.add_text()

    with _config.cvar('players_reached') as players_reached:
        players_reached.add_text()
