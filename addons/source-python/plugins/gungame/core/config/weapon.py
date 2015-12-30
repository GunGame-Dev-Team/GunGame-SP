# ../gungame/core/config/core/weapons.py

"""GunGame weapons configuration."""

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
__all__ = ('multikill_override',
           'order_choose_random',
           'order_file',
           'order_randomize',
           'random_weapon_each_time',
           'randomize_per_player',
           )


# =============================================================================
# >> GLOBAL VARIABLBES
# =============================================================================
_config_strings = LangStrings('gungame/core-configs/weapon')


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager('weapon') as _config:
    with _config.cvar(
            'order_file', 'default_weapon_order',
            _config_strings['Order-File'], ConVarFlags.NOTIFY) as order_file:
        pass

    # TODO: add in functionality
    with _config.cvar(
            'order_choose_random', 0,
            _config_strings['Order-Choose-Random']) as order_choose_random:
        pass

    with _config.cvar(
            'order_randomize', 0, _config_strings['Order-Randomize'],
            ConVarFlags.NOTIFY) as order_randomize:
        pass

    # TODO: add in functionality
    with _config.cvar(
            'randomize_per_player', 0, _config_strings['Randomize-Per-Player'],
            ConVarFlags.NOTIFY) as randomize_per_player:
        pass

    # TODO: add in functionality
    with _config.cvar(
            'random_weapon_each_time', 0, _config_strings['Random-Weapon'],
            ConVarFlags.NOTIFY) as random_weapon_each_time:
        pass

    with _config.cvar(
            'multikill_override', 0, _config_strings['Multikill-Override'],
            ConVarFlags.NOTIFY) as multikill_override:
        pass
