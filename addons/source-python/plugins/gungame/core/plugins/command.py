# ../gungame/core/plugins/command.py

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Plugins
from plugins.command import SubCommandManager

# GunGame Imports
#   Plugins
from gungame.core.plugins import GGPluginsLogger
from gungame.core.plugins.instance import GGLoadedPlugin
from gungame.core.plugins.manager import GGPluginManager
from gungame.core.plugins.queue import PluginQueue
from gungame.core.plugins.valid import ValidPlugins


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
GGPluginsCommandLogger = GGPluginsLogger.command


# =============================================================================
# >> CLASSES
# =============================================================================
class _GGSubCommandManager(SubCommandManager):
    ''''''

    manager = GGPluginManager
    instance = GGLoadedPlugin
    logger = GGPluginsCommandLogger

    def __init__(self, *args, **kwargs):
        ''''''

        # 
        super(_GGSubCommandManager, self).__init__(*args, **kwargs)

        # 
        PluginQueue.prefix = self.prefix

    def load_plugin(self, plugin_name):
        '''Loads a plugin by name.'''
        '''This method is overwritten so that the plugin
            will be loaded after a one tick delay.'''

        # Is the plugin already loaded?
        if plugin_name in self.manager:

            # Is the plugin in the "unload" queue?
            if ('unload' in PluginQueue and
                    plugin_name in PluginQueue['unload']):

                # Remove the plugin from the "unload" queue
                PluginQueue['unload'].discard(plugin_name)

            # No need to go further
            return

        # 
        if not plugin_name in ValidPlugins.all:

            # 
            print('Not a valid plugin!!!')

            # 
            return

        # 
        PluginQueue['load'].add(plugin_name)

    # Set the method's required arguments
    load_plugin.args = ['<plugin>']

    def unload_plugin(self, plugin_name):
        '''Unloads a plugin by name.'''
        '''This method is overwritten so that the plugin
            will be unloaded after a one tick delay.'''

        # Is the plugin loaded?
        if not plugin_name in self.manager:

            # Is the plugin in the "load" queue?
            if 'load' in PluginQueue and plugin_name in PluginQueue['load']:

                # Remove the plugin from the "load" queue
                PluginQueue['load'].discard(plugin_name)

            # No need to go further
            return

        # 
        PluginQueue['unload'].add(plugin_name)

    # Set the method's required arguments
    unload_plugin.args = ['<plugin>']

    def reload_plugin(self, plugin_name=None):
        '''Reloads a plugin by name.'''
        '''This method is overwritten so that the plugin will properly
            be unloaded and loaded after a one tick delay each.'''

        # 
        if plugin_name is None:

            # 
            

            # 
            return

        # 
        if not plugin_name in self.manager:

            # 
            self.load_plugin(plugin_name)

            # 
            return

        # 
        PluginQueue['unload'].add(plugin_name)

        # 
        PluginQueue['reload'].add(plugin_name)

    # Set the method's required arguments
    reload_plugin.args = ['[plugin]']

    def print_version(self):
        ''''''

    def print_credits(self):
        ''''''

    def restart_match(self):
        ''''''

# 
GGSubCommandManager = _GGSubCommandManager('gg', 'GunGame base command.')

# 
GGSubCommandManager['load'] = GGSubCommandManager.load_plugin
GGSubCommandManager['unload'] = GGSubCommandManager.unload_plugin
GGSubCommandManager['reload'] = GGSubCommandManager.reload_plugin

# 
GGSubCommandManager['list'] = GGSubCommandManager.print_plugins
GGSubCommandManager['version'] = GGSubCommandManager.print_version
GGSubCommandManager['credits'] = GGSubCommandManager.print_credits

# 
GGSubCommandManager['restart'] = GGSubCommandManager.restart_match
