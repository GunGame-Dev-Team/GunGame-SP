# ../gungame/core/plugins/command.py

"""Registers the "gg" command."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Cvars
from cvars import ConVar
#   Plugins
from plugins.command import SubCommandManager
#   Translations
from translations.strings import LangStrings

# GunGame Imports
#   Credits
from gungame.core.credits import gungame_credits
#   Plugins
from gungame.core.plugins import _plugin_strings
from gungame.core.plugins import gg_plugins_logger
from gungame.core.plugins.instance import GGLoadedPlugin
from gungame.core.plugins.manager import gg_plugin_manager
from gungame.core.plugins.queue import plugin_queue
from gungame.core.plugins.valid import valid_plugins


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_plugins_command_logger = gg_plugins_logger.command


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('_GGSubCommandManager',
           'gg_command_manager',
           )


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

    def load_plugin(self, plugin_name):
        """Load a plugin by name."""
        # Get the plugin name with the gg_ prefix
        if not plugin_name.startswith('gg_'):
            plugin_name = 'gg_' + plugin_name

        # Is the plugin already loaded?
        if plugin_name in self.manager:

            # Is the plugin in the "unload" queue?
            if ('unload' in plugin_queue and
                    plugin_name in plugin_queue['unload']):

                # Remove the plugin from the "unload" queue
                plugin_queue['unload'].discard(plugin_name)

            # No need to go further
            return

        # Was an invalid plugin name given?
        if plugin_name not in valid_plugins.all:
            print('Not a valid plugin!!!')
            return

        # Add the plugin to the current queue
        plugin_queue['load'].add(plugin_name)

    # Set the method's required arguments
    load_plugin.args = ['<plugin>']

    def unload_plugin(self, plugin_name):
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

            # No need to go further
            return

        # Add the plugin to the current queue
        plugin_queue['unload'].add(plugin_name)

    # Set the method's required arguments
    unload_plugin.args = ['<plugin>']

    def reload_plugin(self, plugin_name):
        """Reload a plugin by name."""
        # Get the plugin name with the gg_ prefix
        if not plugin_name.startswith('gg_'):
            plugin_name = 'gg_' + plugin_name

        # Is the plugin not loaded?
        if plugin_name not in self.manager:

            # Attempt to load the plugin
            self.load_plugin(plugin_name)

            # No need to go further
            return

        # Add the plugin to the unload queue
        plugin_queue['unload'].add(plugin_name)

        # Add the plugin to the reload queue
        plugin_queue['reload'].add(plugin_name)

    # Set the method's required arguments
    reload_plugin.args = ['<plugin>']

    def print_plugins(self):
        """List all currently loaded plugins."""
        # Get header messages
        message = self.prefix + _plugin_strings[
            'Plugins'].get_string() + '\n' + '=' * 61 + '\n'

        # Loop through all loaded plugins
        for plugin_name in sorted(self.manager):

            # Add the plugin's name to the message
            message += '\n{0} ({1}):\n\n'.format(
                plugin_name, valid_plugins.get_plugin_type(plugin_name))

            # Get the plugin's information
            instance = valid_plugins.all[plugin_name]

            # Get the description
            try:
                description = instance.info.description
            except KeyError:
                description = instance.description

            # Add the description
            message += '\tdescription:\n\t\t{0}\n'.format(description)

            # Loop through all items in the info
            for item, value in instance.info.items():

                # Skip the item if it is a LangStrings instance
                if isinstance(value, LangStrings):
                    continue

                # Is the value a ConVar?
                if isinstance(value, ConVar):

                    # Get the ConVar's text
                    value = '{0}:\n\t\t\t{1}: {2}'.format(
                        value.get_name(),
                        value.get_help_text(),
                        value.get_string())

                # Add the current item to the message
                message += '\t{0}:\n\t\t{1}\n'.format(item, value)

            # Add 1 blank line between plugins
            message += '\n'

        # Add the ending separator
        message += '=' * 61

        # Print the message
        self.logger.log_message(message)

    def print_version(self):
        """Print the GunGame version information."""

    def print_credits(self):
        """Print the GunGame credits."""
        # Get header messages
        message = '\n' + self.prefix + _plugin_strings[
            'Credits'].get_string() + '\n' + '=' * 61 + '\n\n'

        # Loop through all groups in the credits
        for group in gungame_credits:

            # Add the current group's name
            message += '\t' + group + ':\n'

            # Loop through all names in the current group
            for name, values in gungame_credits[group].items():

                # Add the current name
                message += '\t\t' + name + ' ' * (
                    20 - len(name)) + values['username'] + '\n'

            # Add 1 blank line between groups
            message += '\n'

        # Print the message
        self.logger.log_message(message + '=' * 61 + '\n\n')

    def restart_match(self):
        """Restart the match."""
        pass

    def unload_all_plugins(self):
        """Unload all plugins when GunGame is unloading."""
        for plugin_name in list(self.manager):
            del self.manager[plugin_name]

# Get the "gg" command instance
gg_command_manager = _GGSubCommandManager('gg', 'GunGame base command.')

# Add the plugin loading sub-commands
gg_command_manager['load'] = gg_command_manager.load_plugin
gg_command_manager['unload'] = gg_command_manager.unload_plugin
gg_command_manager['reload'] = gg_command_manager.reload_plugin

# Add the GunGame information sub-commands
gg_command_manager['list'] = gg_command_manager.print_plugins
gg_command_manager['version'] = gg_command_manager.print_version
gg_command_manager['credits'] = gg_command_manager.print_credits

# Add the restart sub-command
gg_command_manager['restart'] = gg_command_manager.restart_match
