# ../gungame/core/plugins/manager.py

"""Provides a class used to load/unload sub-plugins."""

# =============================================================================
# >> IMPORTS
# =============================================================================
import sys

from plugins.manager import PluginManager

from gungame.core.paths import GUNGAME_PLUGINS_PATH
from gungame.core.plugins import gg_plugins_logger
from gungame.core.plugins.valid import valid_plugins


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_plugins_manager_logger = gg_plugins_logger.manager


# =============================================================================
# >> CLASSES
# =============================================================================
class _GGPluginManager(PluginManager):

    """The GunGame plugin manager class."""

    logger = gg_plugins_manager_logger
    _base_import_prefix = 'gungame.plugins.'

    def __missing__(self, plugin_name):
        """Set the base import path and add the plugin."""
        if plugin_name not in valid_plugins.all:
            raise
        self._base_import = self._base_import_prefix
        self._base_import += valid_plugins.get_plugin_type(plugin_name) + '.'
        return super(_GGPluginManager, self).__missing__(plugin_name)

    def _remove_modules(self, plugin_name):
        """Remove a plugin and all its modules."""
        if plugin_name not in valid_plugins.all:
            raise
        if plugin_name not in self:
            return
        self.base_import = self._base_import
        self.base_import += valid_plugins.get_plugin_type(plugin_name) + '.'
        self._current_plugin = plugin_name
        super(_GGPluginManager, self)._remove_modules(plugin_name)

    def _remove_module(self, module):
        """Remove a module."""
        plugin_path = GUNGAME_PLUGINS_PATH.joinpath(
            valid_plugins.get_plugin_type(self._current_plugin),
            self._current_plugin, '__init__.py')
        if plugin_path == sys.modules[module].__file__:
            return
        super(_GGPluginManager, self)._remove_module(module)

gg_plugin_manager = _GGPluginManager('gungame')
