# ../gungame/gungame.py

"""Weapon leveling game modification."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from cvars.tags import sv_tags
from filters.entities import EntityIter
from listeners.tick import tick_delays

from gungame.info import info
from gungame.core.config.manager import config_manager
from gungame.core.events.storage import gg_resource_list
from gungame.core.plugins.command import gg_command_manager
from gungame.core.weapons.manager import weapon_order_manager


# =============================================================================
# >> LOAD & UNLOAD FUNCTIONS
# =============================================================================
def load():
    """Initialize GunGame."""
    # Initialize GunGame logging

    # Initialize GunGame commands/menus

    # Initialize GunGame weapon orders
    weapon_order_manager.get_weapon_orders()

    # Initialize GunGame events
    gg_resource_list.load_events()

    # Initialize GunGame sounds

    # Initialize GunGame database

    # Initialize GunGame configs
    config_manager.load_configs()

    # Set the starting weapon convars
    weapon_order_manager.set_start_convars()

    # Add gungame to sv_tags
    sv_tags.add(info.basename)

    # Import the listeners/events
    from gungame.listeners import start_match

    # Wait 1 tick to see if gg_start should be called
    tick_delays.delay(0, start_match)


def unload():
    """Clean up GunGame."""
    # Remove gungame from sv_tags
    sv_tags.remove(info.basename)

    # Clean GunGame plugins
    gg_command_manager.unload_all_plugins()

    # Clean GunGame configs

    # Clean GunGame players

    # Clean GunGame database

    # Clean GunGame sounds

    # Clean GunGame events

    # Clean GunGame weapon orders

    # Clean GunGame commands/menus

    # Clean GunGame logging

    # Re-enable buyzones
    for entity in EntityIter('func_buyzone', return_types='entity'):
        entity.enable()
