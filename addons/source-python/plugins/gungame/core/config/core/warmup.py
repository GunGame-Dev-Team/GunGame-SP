# ../gungame/core/config/core/warmup.py

"""GunGame warmup configuration."""

from cvars.flags import ConVarFlags

from gungame.core.config.manager import GunGameConfigManager

with GunGameConfigManager('warmup_settings') as config:
    with config.cvar(
            'gg_warmup_round', 0, ConVarFlags.NONE,
            'Enables/disables GunGame warmup round.') as cvar:
        ...

    with config.cvar(
            'gg_warmup_weapon', 'hegrenade', ConVarFlags.NOTIFY,
            'The weapon to be used in GunGame warmup round.') as cvar:
        ...

    with config.cvar(
            'gg_warmup_time', 30, ConVarFlags.NONE,
            'The number of seconds GunGame warmup round should last.') as cvar:
        ...

    with config.cvar(
            'gg_warmup_min_players', 4, ConVarFlags.NONE,
            'The number of human players required to ' +
            'end warmup round without extending.') as cvar:
        ...

    with config.cvar(
            'gg_warmup_max_extensions', 1, ConVarFlags.NONE,
            'The maximum number of GunGame warmup extensions ' +
            'before starting the match.') as cvar:
        ...

    with config.cvar(
            'gg_warmup_players_reached', 0, ConVarFlags.NONE,
            'Determines when GunGame warmup round should end when the ' +
            'minumum number of players is reached.') as cvar:
        ...

    with config.cvar(
            'gg_warmup_start_config', '', ConVarFlags.NONE,
            'The configuration file that controls the gameplay ' +
            'within GunGame warmup round.') as cvar:
        ...

    with config.cvar(
            'gg_warmup_end_config', '', ConVarFlags.NONE,
            'The configuration file that controls the GunGame '
            "match's settings once warmup round is over.") as cvar:
        ...
