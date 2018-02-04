# ../gungame/core/plugins/queue.py

"""Provides a plugin queue class that loads/unloads plugins."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from contextlib import suppress
from warnings import warn

# Source.Python
from listeners.tick import Delay

# GunGame
from . import gg_plugins_logger
from .manager import gg_plugin_manager
from .valid import plugin_requirements, valid_plugins


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    '_PluginQueue',
    'plugin_queue',
)


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
    logger = gg_plugins_queue_logger
    prefix = None

    def __missing__(self, item):
        """Add the item to its queue and loop through queues after 1 tick."""
        if item not in ('load', 'unload'):
            raise ValueError(f'Invalid plugin type "{item}"')
        if not self:
            Delay(
                delay=0,
                callback=self._loop_through_queues,
            )
        value = self[item] = set()
        return value

    def _loop_through_queues(self):
        """Loop through all queues to properly load/unload plugins."""
        if 'unload' in self:
            self._unload_plugins()
            del self['unload']
        if 'load' not in self:
            return
        self._load_plugins()
        del self['load']

    def _unload_plugins(self):
        """Unload all plugins in the unload queue."""
        # Loop through all plugins to unload
        for plugin_name in self['unload']:

            if plugin_name in plugin_requirements:
                for other in plugin_requirements[plugin_name]:
                    if other in self.manager and other not in self['unload']:
                        warn(
                            f'Plugin "{plugin_name}" is required by "{other}".'
                            f' Please unload "{other}" or load {plugin_name} '
                            'again to avoid issues.'
                        )

            # Unload the plugin
            self.manager.set_base_import(
                value=valid_plugins.get_plugin_type(plugin_name)
            )
            self.manager.unload(plugin_name)

    def _load_plugins(self):
        """Load all plugins in the load queue."""
        # Loop through all plugins to load
        for plugin_name in self['load']:

            # Retrieve the plugin's type
            try:
                plugin_type = valid_plugins.get_plugin_type(plugin_name)
            except ValueError:
                warn(f'Plugin "{plugin_name}" is invalid.')
                continue
            plugin_info = getattr(valid_plugins, plugin_type)[plugin_name].info

            # Check for conflicts
            with suppress(KeyError):
                conflict = False
                for other in plugin_info.get('conflicts', []):
                    if other in self.manager:
                        warn(
                            f'Loaded plugin "{other}" conflicts with plugin '
                            f'"{plugin_name}". Unable to load.'
                        )
                        conflict = True
                if conflict:
                    continue

            # Check for requirements
            with suppress(KeyError):
                for other in plugin_info.get('required', []):
                    if other not in self.manager and other not in self['load']:
                        warn(
                            f'Plugin "{other}" is required by "{plugin_name}".'
                            f' Please load "{other}" to avoid issues.'
                        )

            # Load the plugin and get its instance
            self.manager.set_base_import(plugin_type)
            self.manager.load(plugin_name)

# Get the _PluginQueue instance
plugin_queue = _PluginQueue()
