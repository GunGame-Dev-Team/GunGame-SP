# ../gungame/core/plugins/valid.py

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
from public import public
#   Plugins
from plugins.info import PluginInfo

# GunGame Imports
from gungame.core.plugins.errors import GGPluginFileNotFoundError
from gungame.core.plugins.errors import GGPluginDescriptionMissingError
from gungame.core.plugins.errors import GGPluginInfoMissingError
from gungame.core.plugins.paths import GUNGAME_PLUGIN_PATH


# =============================================================================
# >> CLASSES
# =============================================================================
class ValidPlugin(object):
    def __init__(self, info, description):
        self._info = info
        self._description = description

    @property
    def info(self):
        return self._info

    @property
    def description(self):
        return self._description


@public
class _ValidPlugins(object):
    def __init__(self):
        self._included = self._get_plugins_by_type('included')
        self._custom = self._get_plugins_by_type('custom')
        for plugin in list(self.custom):
            if plugin in self.included:
                del self.custom[plugin]
        self._all = dict(self.included)
        self._all.update(self.custom)

    def get_plugin_type(self, plugin):
        for plugin_type in ('included', 'custom'):
            if plugin in getattr(self, plugin_type):
                return plugin_type
        raise ValueError('No such plugin "{0}"'.format(plugin))

    @property
    def included(self):
        return self._included

    @property
    def custom(self):
        return self._custom

    @property
    def all(self):
        return self._all

    @staticmethod
    def _get_plugins_by_type(plugin_type):
        plugins = {}
        for plugin in GUNGAME_PLUGIN_PATH.joinpath(plugin_type).dirs():
            if plugin.namebase == '__pycache__':
                continue
            if not plugin.joinpath(plugin.namebase + '.py').isfile():
                raise GGPluginFileNotFoundError()
            module = 'gungame.plugins.{0}.{1}'.format(
                plugin_type, plugin.namebase)
            values = __import__(module, fromlist=[''])
            if type(values.__path__).__name__ == '_NamespacePath':
                continue
            for name in values.__dict__:
                if isinstance(values.__dict__[name], PluginInfo):
                    info = values.__dict__[name]
                    break
            else:
                raise GGPluginInfoMissingError()
            if 'translations' in info and 'Description' in info.translations:
                description = info.translations['Description']
            elif values.__doc__:
                description = values.__doc__
            else:
                raise GGPluginDescriptionMissingError()
            plugins[str(plugin.namebase)] = ValidPlugin(info, description)
        return plugins

ValidPlugins = _ValidPlugins()
