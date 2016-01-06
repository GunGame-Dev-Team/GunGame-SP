# ../gungame/core/config/core/warmup.py

"""GunGame warmup configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Cvars
from cvars.flags import ConVarFlags

# GunGame Imports
#   Config
from gungame.core.config.manager import GunGameConfigManager


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('enabled',
           'end_config',
           'max_extensions',
           'min_players',
           'players_reached',
           'start_config',
           'time',
           'weapon',
           )


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager('warmup') as _config:
    with _config.cvar('enabled') as enabled:
        enabled.add_text()

    with _config.cvar(
            'weapon', 'hegrenade', flags=ConVarFlags.NOTIFY) as weapon:
        weapon.add_text()

    with _config.cvar('time', 30) as time:
        time.add_text()

    with _config.cvar('min_players', 4) as min_players:
        min_players.add_text()

    with _config.cvar('max_extensions', 1) as max_extensions:
        max_extensions.add_text()

    with _config.cvar('players_reached') as players_reached:
        players_reached.add_text()

    with _config.cvar('start_config', '') as start_config:
        start_config.add_text()

    with _config.cvar('end_config', '') as end_config:
        end_config.add_text()
