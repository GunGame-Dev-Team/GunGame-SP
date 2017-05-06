# ../gungame/core/commands/registration.py

"""Stores commands with their callbacks."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import defaultdict

# Source.Python
from commands.client import client_command_manager
from commands.say import say_command_manager
from events import Event
from translations.strings import TranslationStrings

# GunGame
from . import commands_ini_file
from .strings import commands_translations


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
command_dictionary = dict()
plugin_commands = defaultdict(list)


# =============================================================================
# >> CLASSES
# =============================================================================
class _RegisteredCommand(object):
    """Class that handles registering of commands."""

    def __init__(self, name, text, callback):
        """Store the commands to be registered."""
        self.name = self.commands = name
        self.callback = callback
        callback_module = self.callback.__module__
        if callback_module.startswith('gungame.plugins'):
            plugin_commands[callback_module.split('.')[3]].append(self.name)
        if self.name in commands_ini_file:
            self.commands = commands_ini_file[self.name].split(',')
            return
        commands_ini_file[self.name] = self.name
        if text in commands_translations:
            text = commands_translations[text]
        if isinstance(text, TranslationStrings):
            text = text.get_string()
        commands_ini_file.comments[self.name] = [''] + text.splitlines()

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
    """Decorator used to register/unregister commands."""
    if name in command_dictionary:
        raise ValueError(
            'Command type "{name}" is already registered.'.format(
                name=name,
            )
        )

    def inner(function):
        """Register the command to the given function."""
        command_dictionary[name] = _RegisteredCommand(name, text, function)
        return function
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


# =============================================================================
# >> EVENTS
# =============================================================================
@Event('gg_plugin_loaded')
def _register_commands(game_event):
    """Register commands for the loaded plugin."""
    plugin = game_event['plugin']
    if plugin not in plugin_commands:
        return
    for name in plugin_commands[plugin]:
        command_dictionary[name].register_commands()


@Event('gg_plugin_unloaded')
def _unregister_commands(game_event):
    """Unregister commands for the unloaded plugin."""
    plugin = game_event['plugin']
    if plugin not in plugin_commands:
        return
    for name in plugin_commands[plugin]:
        command_dictionary[name].unregister_commands()
