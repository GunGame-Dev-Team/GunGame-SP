import sys

from plugins.manager import PluginManager

from gungame.core.plugins import GGPluginsLogger
from gungame.core.plugins.paths import GUNGAME_PLUGIN_PATH
from gungame.core.plugins.valid import ValidPlugins


GGPluginsManagerLogger = GGPluginsLogger.manager


class _GGPluginManager(PluginManager):
    logger = GGPluginsManagerLogger
    _base_import = 'gungame.plugins.'

    def __missing__(self, plugin_name):
        if not plugin_name in ValidPlugins.all:
            raise
        self.base_import = (self._base_import +
            ValidPlugins.get_plugin_type(plugin_name) + '.')
        return super(_GGPluginManager, self).__missing__(plugin_name)

    def _remove_modules(self, plugin_name):
        if not plugin_name in ValidPlugins.all:
            raise
        if not plugin_name in self:
            return
        self.base_import = (self._base_import +
            ValidPlugins.get_plugin_type(plugin_name) + '.')
        self._current_plugin = plugin_name
        super(_GGPluginManager, self)._remove_modules(plugin_name)

    def _remove_module(self, module):
        plugin_path = GUNGAME_PLUGIN_PATH.joinpath(
            ValidPlugins.get_plugin_type(self._current_plugin),
            self._current_plugin, '__init__.py')
        if plugin_path == sys.modules[module].__file__:
            return
        super(_GGPluginManager, self)._remove_module(module)

GGPluginManager = _GGPluginManager('gungame')
