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
#   Engines
from engines.server import engine_server
#   Filters
from filters.entities import EntityIter
#   Listeners
from listeners.tick import Delay
#   Translations
from translations.strings import LangStrings

# GunGame Imports
from gungame.info import info
#   Commands
from gungame.core.commands import register_all_commands
from gungame.core.commands import unregister_all_commands
#   Config
from gungame.core.config.manager import load_all_configs
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
# Get the initialization strings
_base_strings = LangStrings('gungame/load_and_unload')


# =============================================================================
# >> LOAD & UNLOAD FUNCTIONS
# =============================================================================
def load():
    """Initialize GunGame."""
    # Initialize GunGame logging
    # TODO: Make sure to enable logging prior to the start message
    current = 1
    total = len([x for x in _base_strings if x.startswith('Initialize:')])
    gg_logger.log_message(
        _base_strings['Start:Initialize'].get_string(version=info.version))

    # Initialize GunGame weapon orders
    gg_logger.log_message(_base_strings[
        'Initialize:Weapons'].get_string(current=current, total=total))
    current += 1
    weapon_order_manager.get_weapon_orders()

    # Initialize GunGame events
    gg_logger.log_message(_base_strings[
        'Initialize:Events'].get_string(current=current, total=total))
    current += 1
    gg_resource_list.load_events()

    # Initialize GunGame commands/menus
    # TODO: Initialize commands/menus
    gg_logger.log_message(_base_strings[
        'Initialize:Commands'].get_string(current=current, total=total))
    current += 1
    register_all_commands()

    # Initialize GunGame sounds
    # TODO: Initialize sounds
    gg_logger.log_message(_base_strings[
        'Initialize:Sounds'].get_string(current=current, total=total))
    current += 1

    # Initialize GunGame database
    # TODO: Initialize database
    gg_logger.log_message(_base_strings[
        'Initialize:Database'].get_string(current=current, total=total))
    current += 1

    # Initialize GunGame configs
    gg_logger.log_message(_base_strings[
        'Initialize:Configs'].get_string(current=current, total=total))
    current += 1
    load_all_configs()

    # Import the game specific functionality
    gg_logger.log_message(_base_strings[
        'Initialize:Game'].get_string(current=current, total=total))
    current += 1
    with suppress(ImportError):
        import_module('gungame.games.{0}'.format(GAME_NAME))

    # Add gungame to sv_tags
    gg_logger.log_message(_base_strings[
        'Initialize:Tag'].get_string(current=current, total=total))
    current += 1
    sv_tags.add(info.basename)

    # Wait 1 tick to see if gg_start should be called
    gg_logger.log_message(
        _base_strings['End:Initialize'].get_string())

    # Set the starting weapon convars
    weapon_order_manager.set_start_convars()

    # Set the warmup weapon
    warmup_manager.set_warmup_weapon()

    # Set the match status to inactive now that the loading process is complete
    GunGameStatus.MATCH = GunGameMatchStatus.INACTIVE

    # Import the listeners/events/commands/menus
    from gungame.core.listeners import start_match

    Delay(0, start_match)


def unload():
    """Clean up GunGame."""
    # Start the cleanup process
    current = 1
    total = len([x for x in _base_strings if x.startswith('Clean:')])
    gg_logger.log_message(
        _base_strings['Start:Clean'].get_string())

    # Remove gungame from sv_tags
    gg_logger.log_message(_base_strings[
        'Clean:Tag'].get_string(current=current, total=total))
    current += 1
    sv_tags.remove(info.basename)

    # Clean GunGame plugins
    gg_logger.log_message(_base_strings[
        'Clean:Plugins'].get_string(current=current, total=total))
    current += 1
    gg_command_manager.unload_all_plugins()

    # Clean GunGame commands/menus
    gg_logger.log_message(_base_strings[
        'Clean:Commands'].get_string(current=current, total=total))
    current += 1
    unregister_all_commands()

    # Re-enable buyzones
    gg_logger.log_message(_base_strings[
        'Clean:BuyZones'].get_string(current=current, total=total))
    current += 1
    for entity in EntityIter('func_buyzone'):
        entity.enable()

    # Restart the match
    gg_logger.log_message(
        _base_strings['End:Clean'].get_string())
    engine_server.server_command('mp_restartgame 1')
