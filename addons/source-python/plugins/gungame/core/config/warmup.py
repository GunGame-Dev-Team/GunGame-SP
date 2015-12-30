# ../gungame/core/config/core/warmup.py

"""GunGame warmup configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Cvars
from cvars.flags import ConVarFlags
#   Translations
from translations.strings import LangStrings

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
# >> GLOBAL VARIABLBES
# =============================================================================
_config_strings = LangStrings('gungame/core/config/warmup')


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager('warmup') as _config:
    with _config.cvar('enabled', 0, _config_strings['Enabled']) as enabled:
        pass

    with _config.cvar(
            'weapon', 'hegrenade', _config_strings['Weapon'],
            ConVarFlags.NOTIFY) as weapon:
        pass

    with _config.cvar('time', 30, _config_strings['Time']) as time:
        pass

    with _config.cvar(
            'min_players', 4, _config_strings['Min-Players']) as min_players:
        pass

    with _config.cvar(
            'max_extensions', 1,
            _config_strings['Max-Extensions']) as max_extensions:
        pass

    with _config.cvar(
            'players_reached', 0,
            _config_strings['Players-Reached']) as players_reached:
        pass

    with _config.cvar(
            'start_config', '',
            _config_strings['Start-Config']) as start_config:
        pass

    with _config.cvar(
            'end_config', '', _config_strings['End-Config']) as end_config:
        pass
