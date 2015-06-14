# ../gungame/gungame.py

"""Weapon leveling game modification."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Contextlib
from contextlib import suppress
#   Importlib
from importlib import import_module

# Source.Python Imports
#   Core
from core import GAME_NAME
#   Cvars
from cvars.tags import sv_tags
#   Filters
from filters.entities import EntityIter
#   Listeners
from listeners.tick import tick_delays
#   Translations
from translations.strings import LangStrings

# GunGame Imports
from gungame.info import info
#   Config
from gungame.core.config.manager import config_manager
#   Events
from gungame.core.events.storage import gg_resource_list
#   Logger
from gungame.core.logger import gg_logger
#   Plugins
from gungame.core.plugins.command import gg_command_manager
#   Status
from gungame.core.status import GunGameMatchStatus
from gungame.core.status import GunGameStatus
#   Warmup
from gungame.core.warmup import warmup_manager
#   Weapons
from gungame.core.weapons.manager import weapon_order_manager


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_base_strings = LangStrings('gungame/initialization')


# =============================================================================
# >> LOAD & UNLOAD FUNCTIONS
# =============================================================================
def load():
    """Initialize GunGame."""
    # Initialize GunGame logging
    # TODO: Make sure to enable logging prior to the start message
    gg_logger.log_message(
        _base_strings['GunGame_Init_Start'].get_string(version='1.0'))

    # Initialize GunGame weapon orders
    gg_logger.log_message(
        _base_strings['GunGame_Init_Weapons'].get_string())
    weapon_order_manager.get_weapon_orders()

    # Initialize GunGame events
    gg_logger.log_message(
        _base_strings['GunGame_Init_Events'].get_string())
    gg_resource_list.load_events()

    # Initialize GunGame commands/menus
    gg_logger.log_message(
        _base_strings['GunGame_Init_Commands'].get_string())

    # Initialize GunGame sounds
    gg_logger.log_message(
        _base_strings['GunGame_Init_Sounds'].get_string())

    # Initialize GunGame database

    # Initialize GunGame configs
    gg_logger.log_message(
        _base_strings['GunGame_Init_Configs'].get_string())
    config_manager.load_configs()

    # Set the starting weapon convars
    weapon_order_manager.set_start_convars()

    # Set the warmup weapon
    warmup_manager.set_warmup_weapon()

    # Add gungame to sv_tags
    sv_tags.add(info.basename)

    # Import the listeners/events/commands/menus
    from gungame.core.listeners import start_match

    # Set the match status to inactive now that the loading process is complete
    GunGameStatus.MATCH = GunGameMatchStatus.INACTIVE

    # Import the game specific functionality
    gg_logger.log_message(
        _base_strings['GunGame_Init_Game'].get_string())
    with suppress(ImportError):
        import_module('gungame.games.{0}'.format(GAME_NAME))

    # Wait 1 tick to see if gg_start should be called
    gg_logger.log_message(
        _base_strings['GunGame_Init_End'].get_string())
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
