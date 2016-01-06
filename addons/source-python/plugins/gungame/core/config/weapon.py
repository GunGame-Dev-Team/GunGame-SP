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
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager('weapon') as _config:
    with _config.cvar(
            'order_file', 'default_weapon_order',
            flags=ConVarFlags.NOTIFY) as order_file:
        order_file.add_text()

    # TODO: add in functionality
    with _config.cvar('order_choose_random') as order_choose_random:
        order_choose_random.add_text()

    with _config.cvar(
            'order_randomize', flags=ConVarFlags.NOTIFY) as order_randomize:
        order_randomize.add_text()

    # TODO: add in functionality
    with _config.cvar(
            'randomize_per_player',
            flags=ConVarFlags.NOTIFY) as randomize_per_player:
        randomize_per_player.add_text()

    # TODO: add in functionality
    with _config.cvar(
            'random_weapon_each_time',
            flags=ConVarFlags.NOTIFY) as random_weapon_each_time:
        random_weapon_each_time.add_text()

    with _config.cvar(
            'multikill_override',
            flags=ConVarFlags.NOTIFY) as multikill_override:
        multikill_override.add_text()
