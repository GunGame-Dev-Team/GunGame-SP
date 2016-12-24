# ../gungame/core/commands.py

"""Provides player command functionality for menus."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from importlib import import_module

# Source.Python
from commands.client import client_command_manager
from commands.say import say_command_manager

# GunGame
from .paths import GUNGAME_BASE_PATH


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'register_all_commands',
    'unregister_all_commands',
)


# =============================================================================
# >> CLASSES
# =============================================================================
class _MenuCommand(object):
    """Class used to register a command to its menu."""

    def __init__(self, name):
        """Store the base name and send_menu callback."""
        self.name = name
        module = import_module(
            'gungame.core.menus.{menu_name}'.format(
                menu_name=self.name,
            )
        )
        self.send_menu = getattr(
            module,
            'send_{menu_name}_menu'.format(
                menu_name=self.name,
            )
        )

    def register_commands(self):
        """Register the public, private, and client commands."""
        # Register the public commands
        say_command_manager.register_commands(
            (self.name, '!' + self.name),
            _send_command_menu,
        )

        # Register the private command
        say_command_manager.register_commands(
            '/' + self.name,
            _send_command_menu,
        )

        # Register the client command
        client_command_manager.register_commands(
            self.name,
            _send_command_menu,
        )

    def unregister_commands(self):
        """Unregister the public, private, and client commands."""
        # Register the public commands
        say_command_manager.unregister_commands(
            (self.name, '!' + self.name),
            _send_command_menu,
        )

        # Register the private command
        say_command_manager.unregister_commands(
            '/' + self.name,
            _send_command_menu,
        )

        # Register the client command
        client_command_manager.unregister_commands(
            self.name,
            _send_command_menu,
        )


# Get the _CommandManager instance
_command_dictionary = dict()

# Loop through all menus modules
for file in GUNGAME_BASE_PATH.joinpath('core', 'menus').files():

    # Skip private/builtin modules
    if file.namebase.startswith('_'):
        continue

    # Add the command to the dictionary
    _command_dictionary[file.namebase] = _MenuCommand(file.namebase)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def register_all_commands():
    """Register all commands in the dictionary."""
    # Loop through all commands in the dictionary
    for name in _command_dictionary:

        # Register the current command
        _command_dictionary[name].register_commands()


def unregister_all_commands():
    """Unregister all commands in the dictionary."""
    # Loop through all commands in the dictionary
    for name in _command_dictionary:

        # Unregister the current command
        _command_dictionary[name].unregister_commands()


# =============================================================================
# >> CALLBACKS
# =============================================================================
def _send_command_menu(command, index, team_only=None):
    """Send the menu to the player."""
    # Store the block value
    block = False

    # Get the command used
    name = command[0]

    # Does the command have a prefix?
    if name.startswith(('!', '/')):

        # Get the block value
        block = name.startswith('/')

        # Get the actual command name
        name = name[1:]

    # Send the menu
    _command_dictionary[name].send_menu(index)

    # Return the block value
    return block
