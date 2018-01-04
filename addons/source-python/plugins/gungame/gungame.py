# ../gungame/gungame.py

"""Weapon leveling game modification."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from contextlib import suppress
from importlib import import_module

# Source.Python
from core import GAME_NAME
from cvars.tags import sv_tags
from engines.server import queue_command_string
from filters.entities import EntityIter
from listeners.tick import Delay
from translations.strings import LangStrings

# GunGame
from .info import info
from .core.config import load_all_configs
from .core.events.storage import gg_resource_list
from .core.logger import gg_logger
from .core.players.database import winners_database
from .core.plugins.command import gg_command_manager
from .core.rules import define_all_rules
from .core.settings import register_player_settings
from .core.sounds import register_all_sounds
from .core.status import GunGameMatchStatus, GunGameStatus
from .core.weapons.manager import weapon_order_manager


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Get the initialization strings
_base_strings = LangStrings('gungame/load_and_unload')


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    """Initialize GunGame."""
    # Initialize GunGame logging
    # TODO: Make sure to enable logging prior to the start message
    current = 1
    total = len([x for x in _base_strings if x.startswith('Initialize:')])
    gg_logger.log_message(
        _base_strings['Start:Initialize'].get_string(
            version=info.version,
        )
    )

    # Initialize GunGame weapon orders
    gg_logger.log_message(
        _base_strings['Initialize:Weapons'].get_string(
            current=current,
            total=total,
        )
    )
    current += 1
    weapon_order_manager.get_weapon_orders()

    # Initialize GunGame events
    gg_logger.log_message(
        _base_strings['Initialize:Events'].get_string(
            current=current,
            total=total,
        )
    )
    current += 1
    gg_resource_list.load_all_events()

    # Initialize GunGame commands/menus
    gg_logger.log_message(
        _base_strings['Initialize:Commands'].get_string(
            current=current,
            total=total,
        )
    )
    current += 1
    from .core.commands.commands import register_all_commands
    register_all_commands()

    # Initialize GunGame sounds
    gg_logger.log_message(
        _base_strings['Initialize:Sounds'].get_string(
            current=current,
            total=total,
        )
    )
    current += 1
    register_all_sounds()

    # Initialize GunGame database
    gg_logger.log_message(
        _base_strings['Initialize:Database'].get_string(
            current=current,
            total=total,
        )
    )
    current += 1
    winners_database.load_database()

    # Initialize GunGame configs
    gg_logger.log_message(
        _base_strings['Initialize:Configs'].get_string(
            current=current,
            total=total,
        )
    )
    current += 1
    load_all_configs()

    # Initialize GunGame rules
    gg_logger.log_message(
        _base_strings['Initialize:Rules'].get_string(
            current=current,
            total=total,
        )
    )
    current += 1
    define_all_rules()

    # Initialize GunGame player settings
    gg_logger.log_message(
        _base_strings['Initialize:Settings'].get_string(
            current=current,
            total=total,
        )
    )
    current += 1
    register_player_settings()

    # Import the game specific functionality
    gg_logger.log_message(
        _base_strings['Initialize:Game'].get_string(
            current=current,
            total=total,
        )
    )
    current += 1
    with suppress(ImportError):
        import_module(f'gungame.games.{GAME_NAME}')

    # Add gungame to sv_tags
    gg_logger.log_message(
        _base_strings['Initialize:Tag'].get_string(
            current=current,
            total=total,
        )
    )
    current += 1
    sv_tags.add(info.name)

    # Wait 1 tick to see if gg_start should be called
    gg_logger.log_message(
        _base_strings['End:Initialize'].get_string()
    )

    # Set the starting weapon convars
    weapon_order_manager.set_start_convars()

    # Set the match status to inactive now that the loading process is complete
    GunGameStatus.MATCH = GunGameMatchStatus.INACTIVE

    # Import the listeners/events/commands/menus
    from .core.listeners import start_match

    Delay(
        delay=0,
        callback=start_match,
    )


def unload():
    """Clean up GunGame."""
    # Start the cleanup process
    GunGameStatus.MATCH = GunGameMatchStatus.UNLOADING
    current = 1
    total = len([x for x in _base_strings if x.startswith('Clean:')])
    gg_logger.log_message(
        _base_strings['Start:Clean'].get_string()
    )

    # Remove gungame from sv_tags
    gg_logger.log_message(
        _base_strings['Clean:Tag'].get_string(
            current=current,
            total=total,
        )
    )
    current += 1
    sv_tags.remove(info.name)

    # Clean GunGame plugins
    gg_logger.log_message(
        _base_strings['Clean:Plugins'].get_string(
            current=current,
            total=total,
        )
    )
    current += 1
    gg_command_manager.unload_all_plugins()

    # Clean GunGame commands/menus
    gg_logger.log_message(
        _base_strings['Clean:Commands'].get_string(
            current=current,
            total=total,
        )
    )
    current += 1
    from .core.commands.commands import unregister_all_commands
    unregister_all_commands()

    # Re-enable buyzones
    gg_logger.log_message(
        _base_strings['Clean:BuyZones'].get_string(
            current=current,
            total=total,
        )
    )
    current += 1
    for entity in EntityIter('func_buyzone'):
        entity.enable()

    # Restart the match
    gg_logger.log_message(
        _base_strings['End:Clean'].get_string()
    )
    queue_command_string('mp_restartgame 1')
