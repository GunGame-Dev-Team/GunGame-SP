# ../gungame/core/commands/commands.py

"""Registers and unregisters player commands on load/unload."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from .registration import command_dictionary


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
    # Loop through all commands in the dictionary
    for name in command_dictionary:

        # Register the current command
        command_dictionary[name].register_commands()


def unregister_all_commands():
    """Unregister all commands in the dictionary."""
    # Loop through all commands in the dictionary
    for name in command_dictionary:

        # Unregister the current command
        command_dictionary[name].unregister_commands()
