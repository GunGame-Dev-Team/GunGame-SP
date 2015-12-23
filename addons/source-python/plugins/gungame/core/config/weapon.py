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
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager('weapon') as config:
    with config.cvar(
            'order_file', 'default_weapon_order', ConVarFlags.NOTIFY,
            'The weapon order file to use for GunGame.') as order_file:
        pass

    # TODO: add in functionality
    with config.cvar(
            'order_choose_random', 0, ConVarFlags.NONE,
            'Choose a random weapon order each match.') as order_choose_random:
        pass

    with config.cvar(
            'order_randomize', 0, ConVarFlags.NOTIFY,
            'Randomize the weapons in the weapon order.') as order_randomize:
        pass

    # TODO: add in functionality
    with config.cvar(
            'randomize_per_player', 0, ConVarFlags.NOTIFY,
            'If enabled, each player will have a different order to ' +
            'earn their weapons in.') as randomize_per_player:
        pass

    # TODO: add in functionality
    with config.cvar(
            'random_weapon_each_time', 0, ConVarFlags.NOTIFY,
            'If enabled, each time a player is given their level weapon, ' +
            'a different weapon will be chosen from their remaining ' +
            'weapon list.') as random_weapon_each_time:
        pass

    with config.cvar(
            'multikill_override', 0, ConVarFlags.NOTIFY, 'The number of ' +
            'kills all weapons should take to level.') as multikill_override:
        pass
