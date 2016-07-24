# ../gungame/core/plugins/valid.py

"""Provides a class that stores valid plugins by type and name."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from importlib import import_module
from warnings import warn

# GunGame
from ..paths import GUNGAME_PLUGINS_PATH


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'ValidPlugin',
    '_ValidPlugins',
    'valid_plugins',
)


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
        raise ValueError(
            'No such plugin "{plugin_name}".'.format(
                plugin_name=plugin,
            )
        )

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
        # Create a dictionary to store plugins by name
        plugins = dict()

        # Loop through all plugins
        for plugin in GUNGAME_PLUGINS_PATH.joinpath(plugin_type).dirs():

            # Skip the compiled files
            if plugin.namebase == '__pycache__':
                continue

            # Does the primary file not exist?
            if not plugin.joinpath(plugin.namebase + '.py').isfile():
                warn(
                    '{plugin_type} plugin "{plugin_name}" is missing its '
                    'base file.'.format(
                        plugin_type=plugin_type.title(),
                        plugin_name=plugin.namebase,
                    )
                )
                continue

            # Does the info file not exist?
            if not plugin.joinpath('info.py').isfile():
                warn(
                    '{plugin_type} plugin "{plugin_name}" is missing '
                    'info.py file.'.format(
                        plugin_type=plugin_type.title(),
                        plugin_name=plugin.namebase,
                    )
                )
                continue

            # Get the plugin's description
            description = import_module(
                'gungame.plugins.{plugin_type}.{plugin_name}'.format(
                    plugin_type=plugin_type,
                    plugin_name=plugin.namebase,
                )
            ).__doc__

            # Get the plugin's info
            info = import_module(
                'gungame.plugins.{plugin_type}.{plugin_name}.info'.format(
                    plugin_type=plugin_type,
                    plugin_name=plugin.namebase,
                )
            )

            # Does the info have an info attribute?
            if not hasattr(info, 'info'):
                warn(
                    '{plugin_type} plugin "{plugin_name}" info.py does not '
                    'contain an info object.'.format(
                        plugin_type=plugin_type.title(),
                        plugin_name=plugin,
                    )
                )
                continue

            # Add the plugin to the dictionary
            plugins[str(plugin.namebase)] = ValidPlugin(info.info, description)

        # Return the dictionary
        return plugins

# Get the _ValidPlugins instance
valid_plugins = _ValidPlugins()
