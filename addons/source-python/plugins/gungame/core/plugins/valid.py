# ../gungame/core/plugins/valid.py

"""Provides a class that stores valid plugins by type and name."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import defaultdict
from importlib import import_module
from warnings import warn

# Site-package
from configobj import ConfigObj

# Source.Python
from plugins.info import PluginInfo

# GunGame
from ..paths import GUNGAME_PLUGINS_PATH


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'ValidPlugin',
    '_ValidPlugins',
    'plugin_requirements',
    'valid_plugins',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
plugin_requirements = defaultdict(list)


# =============================================================================
# >> CLASSES
# =============================================================================
class ValidPlugin(object):
    """Stores a valid plugin with its information."""

    def __init__(self, info, description):
        """Store the info and description."""
        self.info = info
        self.description = description


class _ValidPlugins(object):
    """Class used to store valid included and custom plugins."""

    def __init__(self):
        """Store all plugins by their type."""
        self.included = self._get_plugins_by_type('included')
        self.custom = self._get_plugins_by_type('custom')
        for plugin in list(self.custom):
            if plugin in self.included:
                del self.custom[plugin]
                warn(
                    'Custom plugin "{plugin_name}" is invalid, as there is '
                    'already an included plugin of the same name.'.format(
                        plugin_name=plugin,
                    )
                )
        self.all = dict(self.included)
        self.all.update(self.custom)

    def get_plugin_type(self, plugin_name):
        """Return the type (included or custom) for the given plugin."""
        for plugin_type in ('included', 'custom'):
            if plugin_name in getattr(self, plugin_type):
                return plugin_type
        raise ValueError(
            'No such plugin "{plugin_name}".'.format(
                plugin_name=plugin_name,
            )
        )

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
            info_file = plugin / 'info.ini'
            if not info_file.isfile():
                warn(
                    '{plugin_type} plugin "{plugin_name}" is missing '
                    'info.ini file.'.format(
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
            info = ConfigObj(info_file)

            # Add the plugin to the dictionary
            plugins[str(plugin.namebase)] = ValidPlugin(info, description)

            required = info.get('required', [])

            for other in required:
                plugin_requirements[other].append(str(plugin.namebase))

        # Return the dictionary
        return plugins

# Get the _ValidPlugins instance
valid_plugins = _ValidPlugins()
