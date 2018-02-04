# ../gungame/core/plugins/command.py

"""Registers the "gg" command."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from contextlib import suppress
from textwrap import TextWrapper

# Source.Python
from plugins.command import SubCommandManager
from translations.strings import LangStrings

# GunGame
from gungame.info import info
from . import plugin_strings, gg_plugins_logger
from .manager import gg_plugin_manager
from .queue import plugin_queue
from .valid import valid_plugins
from ..credits import gungame_credits
from ..messages import message_manager
from ..weapons.manager import weapon_order_manager


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

    def __init__(self, *args, **kwargs):
        """Initialize the instance and set the queue prefix."""
        super().__init__(*args, **kwargs)

        plugin_queue.prefix = self.prefix
        gg_plugin_manager.translations = self.translations

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
        plugin_queue['load'].add(plugin_name)

    def print_plugins(self, index=None):
        """List all currently loaded plugins."""
        # Get header messages
        message = self.prefix + plugin_strings[
            'Plugins'
        ].get_string() + '\n' + '=' * 61 + '\n\n'

        wrapper = TextWrapper(
            width=79,
            initial_indent='',
            subsequent_indent=' ' * 27,
        )

        for plugin_name in sorted(self.manager):
            plugin_info = self.manager[plugin_name].info

            plugin_type = valid_plugins.get_plugin_type(plugin_name)
            message += f'{plugin_name} ({plugin_type}):\n'

            message += f'   title:               {plugin_info.verbose_name}\n'

            if plugin_info.author is not None:
                message += f'   author:              {plugin_info.author}\n'

            if plugin_info.description is not None:
                description = wrapper.wrap(
                    f'   description:         {plugin_info.description}'
                )
                message += '\n'.join(description) + '\n'

            if plugin_info.version != 'unversioned':
                message += f'   version:             {plugin_info.version}\n'

            if plugin_info.url is not None:
                message += f'   url:                 {plugin_info.url}\n'

            if plugin_info.public_convar:
                message += (
                    '   public convar:       '
                    f'{plugin_info.public_convar.name}\n'
                )

            with suppress(KeyError):
                required = '\n                        '.join(
                    plugin_info.required
                )
                message += f'   required plugins:    {required}\n'

            with suppress(KeyError):
                conflicts = '\n                        '.join(
                    plugin_info.conflicts,
                )
                message += f'   plugin conflicts:    {conflicts}\n'

            for attr in plugin_info.display_in_listing:
                message += (
                    f'   {attr}:'.ljust(20) +
                    str(getattr(plugin_info, attr)) + '\n'
                )

            message += '\n'

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
            self.manager.unload(plugin_name, indent=8)

# Get the "gg" command instance
gg_command_manager = _GGSubCommandManager(
    manager=gg_plugin_manager,
    command='gg',
    logger=gg_plugins_command_logger,
)


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
