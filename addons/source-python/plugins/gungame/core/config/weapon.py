# ../gungame/core/config/core/weapons.py

"""GunGame weapons configuration."""

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
            'order_file', 'default_weapon_order', 'The weapon order file ' +
            'to use for GunGame.', ConVarFlags.NOTIFY) as order_file:
        pass

    # TODO: add in functionality
    with _config.cvar(
            'order_choose_random', 0, 'Choose a random ' +
            'weapon order each match.') as order_choose_random:
        pass

    with _config.cvar(
            'order_randomize', 0, 'Randomize the weapons in the weapon order.',
            ConVarFlags.NOTIFY) as order_randomize:
        pass

    # TODO: add in functionality
    with _config.cvar(
            'randomize_per_player', 0, 'If enabled, each player ' +
            'will have a different order to earn their ' +
            'weapons in.', ConVarFlags.NOTIFY) as randomize_per_player:
        pass

    # TODO: add in functionality
    with _config.cvar(
            'random_weapon_each_time', 0, 'If enabled, each time a ' +
            'player is given their level weapon, a different weapon ' +
            'will be chosen from their remaining weapon list.',
            ConVarFlags.NOTIFY) as random_weapon_each_time:
        pass

    with _config.cvar(
            'multikill_override', 0, 'The number of kills all weapons should' +
            ' take to level.', ConVarFlags.NOTIFY) as multikill_override:
        pass
