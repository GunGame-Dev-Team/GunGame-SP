# ../gungame/core/plugins/command.py

"""Registers the "gg" command."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from cvars import ConVar
from plugins.command import SubCommandManager
from translations.strings import LangStrings

# GunGame
from . import plugin_strings, gg_plugins_logger
from .instance import GGLoadedPlugin
from .manager import gg_plugin_manager
from .queue import plugin_queue
from .valid import valid_plugins
from ..credits import gungame_credits
from ..messages import message_manager
from ..weapons.manager import weapon_order_manager
from gungame.info import info


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    '_GGSubCommandManager',
    'gg_command_manager',
    'gg_plugins_command_logger',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_plugins_command_logger = gg_plugins_logger.command

command_strings = LangStrings('gungame/sub_commands')


# =============================================================================
# >> CLASSES
# =============================================================================
class _GGSubCommandManager(SubCommandManager):
    """Class used to integrate the "gg" command."""

    manager = gg_plugin_manager
    instance = GGLoadedPlugin
    logger = gg_plugins_command_logger

    def __init__(self, *args, **kwargs):
        """Initialize the instance and set the queue prefix."""
        # Call the super class' __init__
        super().__init__(*args, **kwargs)

        # Set the queue's prefix
        plugin_queue.prefix = self.prefix

    def load_plugin(self, plugin_name, index=None):
        """Load a plugin by name."""
        # Get the plugin name with the gg_ prefix
        if not plugin_name.startswith('gg_'):
            plugin_name = 'gg_' + plugin_name

        # Is the plugin already loaded?
        if plugin_name in self.manager:

            # Is the plugin in the "unload" queue?
            if (
                'unload' in plugin_queue and
                plugin_name in plugin_queue['unload']
            ):

                # Remove the plugin from the "unload" queue
                plugin_queue['unload'].discard(plugin_name)

            # No need to go further
            return

        # Was an invalid plugin name given?
        if plugin_name not in valid_plugins.all:
            self._send_message(
                self.prefix +
                command_strings['SubCommand:Plugin:Invalid'].get_string(
                    plugin_name=plugin_name,
                ),
                index,
            )
            return

        # Add the plugin to the current queue
        plugin_queue['load'].add(plugin_name)

    def unload_plugin(self, plugin_name, index=None):
        """Unload a plugin by name."""
        # Get the plugin name with the gg_ prefix
        if not plugin_name.startswith('gg_'):
            plugin_name = 'gg_' + plugin_name

        # Is the plugin loaded?
        if plugin_name not in self.manager:

            # Is the plugin in the "load" queue?
            if 'load' in plugin_queue and plugin_name in plugin_queue['load']:

                # Remove the plugin from the "load" queue
                plugin_queue['load'].discard(plugin_name)

            # Was an invalid plugin name given?
            if plugin_name not in valid_plugins.all:
                self._send_message(
                    self.prefix +
                    command_strings['SubCommand:Plugin:Invalid'].get_string(
                        plugin_name=plugin_name,
                    ),
                    index,
                )
                return

            # No need to go further
            return

        # Add the plugin to the current queue
        plugin_queue['unload'].add(plugin_name)

    def reload_plugin(self, plugin_name, index=None):
        """Reload a plugin by name."""
        # Get the plugin name with the gg_ prefix
        if not plugin_name.startswith('gg_'):
            plugin_name = 'gg_' + plugin_name

        # Is the plugin not loaded?
        if plugin_name not in self.manager:

            # Was an invalid plugin name given?
            if plugin_name not in valid_plugins.all:
                self._send_message(
                    self.prefix +
                    command_strings['SubCommand:Plugin:Invalid'].get_string(
                        plugin_name=plugin_name,
                    ),
                    index,
                )
                return

            # Attempt to load the plugin
            self.load_plugin(plugin_name)

            # No need to go further
            return

        # Add the plugin to the unload queue
        plugin_queue['unload'].add(plugin_name)

        # Add the plugin to the reload queue
        plugin_queue['reload'].add(plugin_name)

    def print_plugins(self, index=None):
        """List all currently loaded plugins."""
        # Get header messages
        message = self.prefix + plugin_strings[
            'Plugins'
        ].get_string() + '\n' + '=' * 61 + '\n'

        loaded_included = sorted([
            name for name in self.manager if name in valid_plugins.included
        ])
        loaded_custom = sorted([
            name for name in self.manager if name in valid_plugins.custom
        ])
        for plugin_name in loaded_included + loaded_custom:

            # Add the plugin's name to the message
            message += '\n{plugin_name} ({plugin_type}):\n\n'.format(
                plugin_name=plugin_name,
                plugin_type=valid_plugins.get_plugin_type(plugin_name),
            )

            # Get the plugin's information
            instance = valid_plugins.all[plugin_name]

            # Get the description
            try:
                description = instance.info.description
            except KeyError:
                description = instance.description

            # Add the description
            message += '\tdescription:\n\t\t{description}\n'.format(
                description=description,
            )

            # Loop through all items in the info
            for item, value in instance.info.items():

                # Skip the item if it is a LangStrings instance
                if isinstance(value, LangStrings):
                    continue

                # Is the value a ConVar?
                if isinstance(value, ConVar):

                    # Get the ConVar's text
                    value = '{cvar_name}:\n\t\t\t{help_text}: {value}'.format(
                        cvar_name=value.name,
                        help_text=value.help_text,
                        value=value.get_string(),
                    )

                # Add the current item to the message
                message += '\t{item}:\n\t\t{value}\n'.format(
                    item=item,
                    value=value,
                )

            # Add 1 blank line between plugins
            message += '\n'

        # Add the ending separator
        message += '=' * 61

        # Print the message
        self._send_message(message, index)

    def print_version(self, index=None):
        """Print the GunGame version information."""
        self._send_message(
            self.prefix + command_strings['SubCommand:Version'].get_string(
                version=info.version,
            ),
            index
        )

    def print_credits(self, index=None):
        """Print the GunGame credits."""
        # Get header messages
        message = '\n' + self.prefix + plugin_strings[
            'Credits'
        ].get_string() + '\n' + '=' * 61 + '\n\n'

        # Loop through all groups in the credits
        for group in gungame_credits:

            # Add the current group's name
            message += '\t' + group + ':\n'

            # Loop through all names in the current group
            for name, values in gungame_credits[group].items():

                # Add the current name
                message += '\t\t' + name + ' ' * (
                    20 - len(name)
                ) + values['username'] + '\n'

            # Add 1 blank line between groups
            message += '\n'

        # Print the message
        self._send_message(message + '=' * 61 + '\n\n', index)

    @staticmethod
    def restart_match():
        """Restart the match."""
        weapon_order_manager.restart_game()

    def _send_message(self, message, index):
        if index is None:
            self.logger.log_message(message)
        else:
            for line in message.splitlines():
                message_manager.echo_message(line, index)

    def unload_all_plugins(self):
        """Unload all plugins when GunGame is unloading."""
        for plugin_name in list(self.manager):
            del self.manager[plugin_name]

# Get the "gg" command instance
gg_command_manager = _GGSubCommandManager('gg')


@gg_command_manager.server_sub_command(['plugin', 'load'])
@gg_command_manager.client_sub_command(['plugin', 'load'], 'gungame.load')
def _gg_plugin_load(command_info, plugin):
    gg_command_manager.load_plugin(plugin, command_info.index)


@gg_command_manager.server_sub_command(['plugin', 'unload'])
@gg_command_manager.client_sub_command(['plugin', 'unload'], 'gungame.unload')
def _gg_plugin_unload(command_info, plugin):
    gg_command_manager.unload_plugin(plugin, command_info.index)


@gg_command_manager.server_sub_command(['plugin', 'reload'])
@gg_command_manager.client_sub_command(['plugin', 'reload'], 'gungame.reload')
def _gg_plugin_reload(command_info, plugin):
    gg_command_manager.reload_plugin(plugin, command_info.index)


@gg_command_manager.server_sub_command(['plugin', 'list'])
@gg_command_manager.client_sub_command(['plugin', 'list'])
def _gg_plugin_list(command_info):
    gg_command_manager.print_plugins(command_info.index)


@gg_command_manager.server_sub_command(['version'])
@gg_command_manager.client_sub_command(['version'])
def _gg_version(command_info):
    gg_command_manager.print_version(command_info.index)


@gg_command_manager.server_sub_command(['credits'])
@gg_command_manager.client_sub_command(['credits'])
def _gg_credits(command_info):
    gg_command_manager.print_credits(command_info.index)


@gg_command_manager.server_sub_command(['restart'])
@gg_command_manager.client_sub_command(['restart'], 'gungame.restart')
def _gg_restart(command_info):
    gg_command_manager.restart_match()
