# ../gungame/core/commands/commands.py

"""Registers and unregisters player commands on load/unload."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from itertools import chain

# GunGame
from .registration import command_dictionary, plugin_commands


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'register_all_commands',
    'unregister_all_commands',
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def register_all_commands():
    """Register all commands in the dictionary."""
    plugin_command_list = list(chain.from_iterable(plugin_commands.values()))
    for name in command_dictionary:
        if name in plugin_command_list:
            continue
        command_dictionary[name].register_commands()


def unregister_all_commands():
    """Unregister all commands in the dictionary."""
    plugin_command_list = list(chain.from_iterable(plugin_commands.values()))
    for name in command_dictionary:
        if name in plugin_command_list:
            continue
        command_dictionary[name].unregister_commands()
