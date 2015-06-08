# ../gungame/core/plugins/valid.py

"""Provides a class that stores valid plugins by type and name."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from importlib import import_module

# Source.Python Imports
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

    """Stores a valid plugin with its information."""

    def __init__(self, info, description):
        """Store the info and description."""
        self._info = info
        self._description = description

    @property
    def info(self):
        """Return the plugin's info instance."""
        return self._info

    @property
    def description(self):
        """Return the plugin's description."""
        return self._description


class _ValidPlugins(object):

    """Class used to store valid included and custom plugins."""

    def __init__(self):
        """Store all plugins by their type."""
        self._included = self._get_plugins_by_type('included')
        self._custom = self._get_plugins_by_type('custom')
        for plugin in list(self.custom):
            if plugin in self.included:
                del self.custom[plugin]
        self._all = dict(self.included)
        self._all.update(self.custom)

    def get_plugin_type(self, plugin):
        """Return the type (included or custom) for the given plugin."""
        for plugin_type in ('included', 'custom'):
            if plugin in getattr(self, plugin_type):
                return plugin_type
        raise ValueError('No such plugin "{0}"'.format(plugin))

    @property
    def included(self):
        """Return the included plugins."""
        return self._included

    @property
    def custom(self):
        """Return the custom plugins."""
        return self._custom

    @property
    def all(self):
        """Return all of the plugins."""
        return self._all

    @staticmethod
    def _get_plugins_by_type(plugin_type):
        """Store each plugin for the given type."""
        plugins = {}
        for plugin in GUNGAME_PLUGIN_PATH.joinpath(plugin_type).dirs():
            if plugin.namebase == '__pycache__':
                continue
            if not plugin.joinpath(plugin.namebase + '.py').isfile():
                raise GGPluginFileNotFoundError()
            module = 'gungame.plugins.{0}.{1}'.format(
                plugin_type, plugin.namebase)
            values = import_module(module)
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

valid_plugins = _ValidPlugins()
