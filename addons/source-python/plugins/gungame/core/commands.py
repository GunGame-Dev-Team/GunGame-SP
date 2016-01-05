# ../gungame/core/commands.py

"""Provides player command functionality for menus."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Importlib
from importlib import import_module

# Source.Python Imports
#   Commands
from commands.client import client_command_manager
from commands.say import say_command_manager

# GunGame Imports
#   Paths
from gungame.core.paths import GUNGAME_BASE_PATH


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('command_manager',
           )


# =============================================================================
# >> CLASSES
# =============================================================================
class _MenuCommand(object):
    """Class used to register a command to its menu."""

    def __init__(self, name):
        """Store the base name and send_menu callback."""
        self._name = name
        module = import_module('gungame.core.menus.{0}'.format(self.name))
        self.send_menu = getattr(module, 'send_{0}_menu'.format(self.name))

    @property
    def name(self):
        """Return the base name of the command."""
        return self._name

    def register_commands(self):
        """Register the public, private, and client commands."""
        # Register the public commands
        say_command_manager.register_commands(
            (self.name, '!' + self.name), _send_command_menu)

        # Register the private command
        say_command_manager.register_commands(
            '/' + self.name, _send_command_menu_private)

        # Register the client command
        client_command_manager.register_commands(
            self.name, _send_command_menu)

    def unregister_commands(self):
        """Unregister the public, private, and client commands."""
        # Register the public commands
        say_command_manager.unregister_commands(
            (self.name, '!' + self.name), _send_command_menu)

        # Register the private command
        say_command_manager.unregister_commands(
            '/' + self.name, _send_command_menu_private)

        # Register the client command
        client_command_manager.unregister_commands(
            self.name, _send_command_menu)


class _CommandManager(dict):
    """Dictionary class used to store commands."""

    def __init__(self):
        """Add all commands to the dictionary."""
        # Initialize the dictionary
        super().__init__()

        # Loop through all menus modules
        for file in GUNGAME_BASE_PATH.joinpath('core', 'menus').files():

            # Skip private/builtin modules
            if file.namebase.startswith('_'):
                continue

            # Add the command to the dictionary
            self[file.namebase] = _MenuCommand(file.namebase)

    def register_commands(self):
        """Register all commands in the dictionary."""
        # Loop through all commands in the dictionary
        for name in self:

            # Register the current command
            self[name].register_commands()

    def unregister_commands(self):
        """Unregister all commands in the dictionary."""
        # Loop through all commands in the dictionary
        for name in self:

            # Unregister the current command
            self[name].unregister_commands()

# Get the _CommandManager instance
command_manager = _CommandManager()


# =============================================================================
# >> CALLBACKS
# =============================================================================
def _send_command_menu(command, index, team_only=None):
    """Send the menu to the player."""
    command_manager[_get_command(command)].send_menu(index)


def _send_command_menu_private(command, index, team_only):
    """Send the command to the player and suppress the chat message."""
    # Send the menu
    _send_command_menu(command, index)

    # Stop the command from showing in chat
    return False


def _get_command(command):
    """Return the command used."""
    # Get the command used
    command = command[0]

    # Does the command have a prefix?
    if command.startswith(('!', '/')):

        # Return the command without the prefix
        return command[1:]

    # Return the command
    return command
