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
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager('warmup') as config:
    with config.cvar(
            'enabled', 0, ConVarFlags.NONE,
            'Enables/disables GunGame warmup round.') as enabled:
        ...

    with config.cvar(
            'weapon', 'hegrenade', ConVarFlags.NOTIFY,
            'The weapon to be used in GunGame warmup round.') as weapon:
        ...

    with config.cvar(
            'time', 30, ConVarFlags.NONE,
            'The number of seconds GunGame warmup round should last.') as time:
        ...

    with config.cvar(
            'min_players', 4, ConVarFlags.NONE,
            'The number of human players required to ' +
            'end warmup round without extending.') as min_players:
        ...

    with config.cvar(
            'max_extensions', 1, ConVarFlags.NONE,
            'The maximum number of GunGame warmup extensions ' +
            'before starting the match.') as max_extensions:
        ...

    with config.cvar(
            'players_reached', 0, ConVarFlags.NONE,
            'Determines when GunGame warmup round should end when the ' +
            'minumum number of players is reached.') as players_reached:
        ...

    with config.cvar(
            'start_config', '', ConVarFlags.NONE,
            'The configuration file that controls the gameplay ' +
            'within GunGame warmup round.') as start_config:
        ...

    with config.cvar(
            'end_config', '', ConVarFlags.NONE,
            'The configuration file that controls the GunGame '
            "match's settings once warmup round is over.") as end_config:
        ...
