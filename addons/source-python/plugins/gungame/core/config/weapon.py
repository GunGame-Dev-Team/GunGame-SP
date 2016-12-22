# ../gungame/core/config/weapon.py

"""GunGame weapons configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from cvars.flags import ConVarFlags

# GunGame
from ..config.manager import GunGameConfigManager


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'multi_kill_override',
    'order_choose_random',
    'order_file',
    'order_randomize',
    'prop_physics',
    'random_weapon_each_time',
    'randomize_per_player',
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager('weapon') as _config:
    with _config.cvar(
        'order_file', 'default', flags=ConVarFlags.NOTIFY,
    ) as order_file:
        order_file.add_text()

    # TODO: add in functionality
    with _config.cvar('order_choose_random') as order_choose_random:
        order_choose_random.add_text()

    with _config.cvar(
        'order_randomize', flags=ConVarFlags.NOTIFY,
    ) as order_randomize:
        order_randomize.add_text()

    # TODO: add in functionality
    with _config.cvar(
        'randomize_per_player', flags=ConVarFlags.NOTIFY,
    ) as randomize_per_player:
        randomize_per_player.add_text()

    # TODO: add in functionality
    with _config.cvar(
        'random_weapon_each_time', flags=ConVarFlags.NOTIFY,
    ) as random_weapon_each_time:
        random_weapon_each_time.add_text()

    with _config.cvar(
        'multi_kill_override', flags=ConVarFlags.NOTIFY,
    ) as multi_kill_override:
        multi_kill_override.add_text()

    with _config.cvar('prop_physics') as prop_physics:
        prop_physics.add_text()
