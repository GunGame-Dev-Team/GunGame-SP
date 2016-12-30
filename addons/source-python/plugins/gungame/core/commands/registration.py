# ../gungame/core/commands/callbacks.py

"""Stores commands with their callbacks."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from configobj import ConfigObj

from commands.client import client_command_manager
from commands.say import say_command_manager
from translations.strings import TranslationStrings

from . import command_strings
from ..paths import GUNGAME_CFG_PATH


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_commands_ini = ConfigObj(GUNGAME_CFG_PATH / 'commands.ini')
if not _commands_ini:
    _commands_ini.initial_comment = (
        command_strings['Commands:Header'].get_string().splitlines()
    )

command_dictionary = dict()


# =============================================================================
# >> CLASSES
# =============================================================================
class _RegisteredCommand(object):
    def __init__(self, name, text, callback):
        self.name = self.commands = name
        self.callback = callback
        if self.name in _commands_ini:
            self.commands = _commands_ini[self.name].split(',')
            return
        _commands_ini[self.name] = self.name
        if isinstance(text, TranslationStrings):
            text = text.get_string()
        _commands_ini.comments[self.name] = [''] + text.splitlines()

    def register_commands(self):
        """Register the public, private, and client commands."""
        for command in self.commands:
            # Register the public commands
            say_command_manager.register_commands(
                (command, '!' + command),
                _send_command_menu,
            )

            # Register the private command
            say_command_manager.register_commands(
                '/' + command,
                _send_command_menu,
            )

            # Register the client command
            client_command_manager.register_commands(
                command,
                _send_command_menu,
            )

    def unregister_commands(self):
        """Unregister the public, private, and client commands."""
        for command in self.commands:
            # Unregister the public commands
            say_command_manager.unregister_commands(
                (command, '!' + command),
                _send_command_menu,
            )

            # Unregister the private command
            say_command_manager.unregister_commands(
                '/' + command,
                _send_command_menu,
            )

            # Unregister the client command
            client_command_manager.unregister_commands(
                command,
                _send_command_menu,
            )


# =============================================================================
# >> DECORATOR FUNCTIONS
# =============================================================================
def register_command_callback(name, text):
    if name in command_dictionary:
        raise ValueError(
            'Command type "{name}" is already registered.'.format(
                name=name,
            )
        )

    def inner(function):
        command_dictionary[name] = _RegisteredCommand(name, text, function)
    return inner


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
    command_dictionary[name].callback(index)

    # Return the block value
    return block
