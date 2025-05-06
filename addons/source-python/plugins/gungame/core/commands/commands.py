# ../gungame/core/commands/commands.py

"""Registers and unregisters player commands on load/unload."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from importlib import import_module
from itertools import chain

# GunGame
from . import commands_ini_file
from .registration import command_dictionary, plugin_commands
from .strings import commands_translations
from ..paths import GUNGAME_BASE_PATH
from ..plugins.valid import valid_plugins

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "find_all_commands",
    "load_all_commands",
    "unload_all_commands",
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def find_all_commands():
    """Find all included and plugin commands."""
    if not commands_ini_file:
        commands_ini_file.initial_comment = (
            commands_translations["Commands:Header"].get_string().splitlines()
        )
    menus_path = GUNGAME_BASE_PATH / "core" / "menus"
    for file_path in menus_path.files():
        if file_path.stem.startswith("_"):
            continue
        import_module(f"gungame.core.menus.{file_path.stem}")

    import_module("gungame.core.rules.command")

    for plugin_name in valid_plugins.all:
        plugin_path = valid_plugins.get_plugin_path(plugin_name)
        plugin_type = str(plugin_path.parent.stem)
        commands_path = plugin_path / "commands.py"
        if commands_path.is_file():
            import_module(
                f"gungame.plugins.{plugin_type}.{plugin_name}.commands",
            )

    commands_ini_file.write()


def load_all_commands():
    """Register all commands in the dictionary."""
    plugin_command_list = list(chain.from_iterable(plugin_commands.values()))
    for name, instance in command_dictionary.items():
        if name in plugin_command_list:
            continue
        instance.register_commands()


def unload_all_commands():
    """Unregister all commands in the dictionary."""
    plugin_command_list = list(chain.from_iterable(plugin_commands.values()))
    for name, instance in command_dictionary.items():
        if name in plugin_command_list:
            continue
        instance.unregister_commands()
