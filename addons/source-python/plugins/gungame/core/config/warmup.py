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
    with _config.cvar(
            'enabled', 0, 'Enables/disables GunGame warmup round.') as enabled:
        pass

    with _config.cvar(
            'weapon', 'hegrenade', 'The weapon to be used in GunGame ' +
            'warmup round.', ConVarFlags.NOTIFY) as weapon:
        pass

    with _config.cvar(
            'time', 30, 'The number of seconds GunGame warmup ' +
            'round should last.') as time:
        pass

    with _config.cvar(
            'min_players', 4, 'The number of human players required to ' +
            'end warmup round without extending.') as min_players:
        pass

    with _config.cvar(
            'max_extensions', 1, 'The maximum number of GunGame warmup ' +
            'extensions before starting the match.') as max_extensions:
        pass

    with _config.cvar(
            'players_reached', 0, 'Determines when GunGame warmup round ' +
            'should end when the minumum number of players is ' +
            'reached.') as players_reached:
        pass

    with _config.cvar(
            'start_config', '', 'The configuration file that controls the ' +
            'gameplay within GunGame warmup round.') as start_config:
        pass

    with _config.cvar(
            'end_config', '', 'The configuration file that controls the ' +
            "GunGame match's settings once warmup round is " +
            'over.') as end_config:
        pass
