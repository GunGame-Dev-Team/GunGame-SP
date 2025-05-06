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
    "ValidPlugin",
    "_ValidPlugins",
    "plugin_requirements",
    "valid_plugins",
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
plugin_requirements = defaultdict(list)


# =============================================================================
# >> CLASSES
# =============================================================================
class ValidPlugin:
    """Stores a valid plugin with its information."""

    def __init__(self, info, description):
        """Store the info and description."""
        self.info = info
        self.description = description


class _ValidPlugins:
    """Class used to store valid included and custom plugins."""

    def __init__(self):
        """Store all plugins by their type."""
        self.included = self._get_plugins_by_type("included")
        self.custom = self._get_plugins_by_type("custom")
        for plugin in list(self.custom):
            if plugin in self.included:
                del self.custom[plugin]
                warn(
                    f'Custom plugin "{plugin}" is invalid, as there is '
                    'already an included plugin of the same name.',
                    stacklevel=2,
                )
        self.all = dict(self.included)
        self.all.update(self.custom)

    def get_plugin_type(self, plugin_name):
        """Return the type (included or custom) for the given plugin."""
        for plugin_type in ("included", "custom"):
            if plugin_name in getattr(self, plugin_type):
                return plugin_type
        msg = f'No such plugin "{plugin_name}".'
        raise ValueError(msg)

    def get_plugin_path(self, plugin_name):
        """Return the path for the sub-plugin."""
        plugin_type = self.get_plugin_type(plugin_name)
        return GUNGAME_PLUGINS_PATH / plugin_type / plugin_name

    @staticmethod
    def _get_plugins_by_type(plugin_type):
        """Store each plugin for the given type."""
        # Create a dictionary to store plugins by name
        plugins = {}

        # Loop through all plugins
        type_path = GUNGAME_PLUGINS_PATH / plugin_type
        for plugin in type_path.dirs():

            # Skip the compiled files
            if plugin.stem == "__pycache__":
                continue

            # Does the primary file not exist?
            plugin_path = plugin / plugin.stem + ".py"
            if not plugin_path.is_file():
                warn(
                    f'{plugin_type.title()} plugin "{plugin.stem}" '
                    'is missing its base file.',
                    stacklevel=2,
                )
                continue

            # Does the info file not exist?
            info_file = plugin / "info.ini"
            if not info_file.is_file():
                warn(
                    f'{plugin_type.title()} plugin "{plugin.stem}" '
                    'is missing info.ini file.',
                    stacklevel=2,
                )
                continue

            # Get the plugin's description
            description = import_module(
                f"gungame.plugins.{plugin_type}.{plugin.stem}",
            ).__doc__

            # Get the plugin's info
            info = ConfigObj(info_file)

            # Add the plugin to the dictionary
            plugins[str(plugin.stem)] = ValidPlugin(info, description)

            required = info.get("required", [])

            for other in required:
                plugin_requirements[other].append(str(plugin.stem))

        # Return the dictionary
        return plugins


valid_plugins = _ValidPlugins()
