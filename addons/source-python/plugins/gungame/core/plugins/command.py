# ../gungame/core/plugins/command.py

"""Registers the "gg" command."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Plugins
from plugins.command import SubCommandManager

# Script Imports
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
        super(_GGSubCommandManager, self).__init__(*args, **kwargs)

        # Set the queue's prefix
        plugin_queue.prefix = self.prefix

    def load_plugin(self, plugin_name):
        """Load a plugin by name.

        This method is overwritten so that the plugin
            will be loaded after a one tick delay.
        """
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
        """Unload a plugin by name.

        This method is overwritten so that the plugin
            will be unloaded after a one tick delay.
        """
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
        """Reload a plugin by name.

        This method is overwritten so that the plugin will properly
            be unloaded and loaded after a one tick delay each.
        """
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
    reload_plugin.args = ['[plugin]']

    def print_version(self):
        """Print the GunGame version information."""

    def print_credits(self):
        """Print the GunGame credits."""

    def restart_match(self):
        """Restart the match."""
        pass

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
