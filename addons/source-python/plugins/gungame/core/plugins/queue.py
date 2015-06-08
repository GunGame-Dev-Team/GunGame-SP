# ../gungame/core/plugins/queue.py

"""Provides a plugin queue class that loads/unloads plugins."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from tick.delays import TickDelays

from gungame.core.plugins import gg_plugins_logger
from gungame.core.plugins.manager import gg_plugin_manager


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_plugins_queue_logger = gg_plugins_logger.queue


# =============================================================================
# >> CLASSES
# =============================================================================
class _PluginQueue(dict):

    """Plugin queue class used to load/unload plugins."""

    manager = gg_plugin_manager
    translations = manager.translations
    logger = gg_plugins_queue_logger

    def __missing__(self, item):
        """Add the item to its queue and loop through queues after 1 tick."""
        if item not in ('load', 'unload', 'reload'):
            raise ValueError('Invalid plugin type "{0}"'.format(item))
        if not self:
            TickDelays.delay(0, self._loop_through_queues)
        value = self[item] = set()
        return value

    def _loop_through_queues(self):
        """Loop through all queues to properly load/unload plugins."""
        if 'unload' in self:
            self._unload_plugins()
            del self['unload']
        if 'load' in self:
            self._load_plugins()
            del self['load']
        if 'reload' not in self:
            return
        self['load'] = set(self['reload'])
        del self['reload']

    def _unload_plugins(self):
        """Unload all plugins in the unload queue."""
        # Loop through all plugins to unload
        for plugin_name in self['unload']:

            # Unload the plugin
            del gg_plugin_manager[plugin_name]

            # Send a message that the plugin was unloaded
            self.logger.log_message(self.prefix + self.translations[
                'Successful Unload'].get_string(plugin=plugin_name))

    def _load_plugins(self):
        """Load all plugins in the load queue."""
        # Loop through all plugins to load
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

# Get the _PluginQueue instance
plugin_queue = _PluginQueue()
