# ../gungame/core/plugins/queue.py

# =============================================================================
# >> IMPORTS
# =============================================================================
from tick.delays import TickDelays

from gungame.core.plugins import GGPluginsLogger
from gungame.core.plugins.manager import GGPluginManager


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
GGPluginsQueueLogger = GGPluginsLogger.queue


# =============================================================================
# >> CLASSES
# =============================================================================
class _PluginQueue(dict):
    ''''''

    manager = GGPluginManager
    translations = manager.translations
    logger = GGPluginsQueueLogger

    def __missing__(self, item):
        if not item in ('load', 'unload', 'reload'):
            raise ValueError('Invalid plugin type "{0}"'.format(item))
        if not self:
            TickDelays.delay(0, self._loop_through_queues)
        value = self[item] = set()
        return value

    def _loop_through_queues(self):
        if 'unload' in self:
            self._unload_plugins()
            del self['unload']
        if 'load' in self:
            self._load_plugins()
            del self['load']
        if not 'reload' in self:
            return
        self['load'] = set(self['reload'])
        del self['reload']

    def _unload_plugins(self):
        ''''''

        # Loop through all plugins to unload
        for plugin_name in self['unload']:

            # Unload the plugin
            del GGPluginManager[plugin_name]

            # Send a message that the plugin was unloaded
            self.logger.log_message(self.prefix + self.translations[
                'Successful Unload'].get_string(plugin=plugin_name))

    def _load_plugins(self):
        ''''''

        # 
        for plugin_name in self['load']:

            # Load the plugin and get its instance
            plugin = self.manager[plugin_name]

            # Was the plugin unable to be loaded?
            if plugin is None:

                # Send a message that the plugin was not loaded
                self.logger.log_message(self.prefix + self.translations[
                    'Unable to Load'].get_string(plugin=plugin_name))

                # No need to go further
                return

            # Send a message that the plugin was loaded
            self.logger.log_message(self.prefix + self.translations[
                'Successful Load'].get_string(plugin=plugin_name))

# Get the PluginQueue instance
PluginQueue = _PluginQueue()
