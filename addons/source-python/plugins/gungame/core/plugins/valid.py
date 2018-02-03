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
                    f'Custom plugin "{plugin}" is invalid, as there is '
                    'already an included plugin of the same name.'
                )
        self.all = dict(self.included)
        self.all.update(self.custom)

    def get_plugin_type(self, plugin_name):
        """Return the type (included or custom) for the given plugin."""
        for plugin_type in ('included', 'custom'):
            if plugin_name in getattr(self, plugin_type):
                return plugin_type
        raise ValueError(f'No such plugin "{plugin_name}".')

    def get_plugin_path(self, plugin_name):
        """Return the path for the sub-plugin."""
        plugin_type = self.get_plugin_type(plugin_name)
        return GUNGAME_PLUGINS_PATH / plugin_type / plugin_name

    @staticmethod
    def _get_plugins_by_type(plugin_type):
        """Store each plugin for the given type."""
        # Create a dictionary to store plugins by name
        plugins = dict()

        # Loop through all plugins
        type_path = GUNGAME_PLUGINS_PATH / plugin_type
        for plugin in type_path.dirs():

            # Skip the compiled files
            if plugin.namebase == '__pycache__':
                continue

            # Does the primary file not exist?
            plugin_path = plugin / plugin.namebase + '.py'
            if not plugin_path.isfile():
                warn(
                    f'{plugin_type.title()} plugin "{plugin.namebase}" '
                    'is missing its base file.'
                )
                continue

            # Does the info file not exist?
            info_file = plugin / 'info.ini'
            if not info_file.isfile():
                warn(
                    f'{plugin_type.title()} plugin "{plugin.namebase}" '
                    'is missing info.ini file.'
                )
                continue

            # Get the plugin's description
            description = import_module(
                f'gungame.plugins.{plugin_type}.{plugin.namebase}'
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
