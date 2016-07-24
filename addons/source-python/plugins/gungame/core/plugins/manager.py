# ../gungame/core/plugins/manager.py

"""Provides a class used to load/unload sub-plugins."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
import sys

# Source.Python
from plugins.manager import PluginManager

# GunGame
from ..events.included.plugins import GG_Plugin_Unloaded
from ..paths import GUNGAME_PLUGINS_PATH
from . import gg_plugins_logger
from .valid import valid_plugins


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_plugins_manager_logger = gg_plugins_logger.manager


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    '_GGPluginManager',
    'gg_plugin_manager',
)


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
            raise ValueError(
                'Invalid plugin_name "{plugin_name}".'.format(
                    plugin_name=plugin_name,
                )
            )
        plugin_type = valid_plugins.get_plugin_type(plugin_name)
        self._base_import = self._base_import_prefix + plugin_type + '.'
        return super().__missing__(plugin_name)

    def __delitem__(self, plugin_name):
        """Unload the plugin and remove it from the dictionary."""
        # Unload the plugin
        super().__delitem__(plugin_name)

        # Send a message that the plugin was unloaded
        self.logger.log_message(
            self.prefix + self.translations[
                'Successful Unload'
            ].get_string(plugin=plugin_name)
        )

        # Fire the gg_plugin_unloaded event
        with GG_Plugin_Unloaded() as event:
            event.plugin = plugin_name
            event.plugin_type = valid_plugins.get_plugin_type(plugin_name)

    def _remove_modules(self, plugin_name):
        """Remove a plugin and all its modules."""
        if plugin_name not in valid_plugins.all:
            raise ValueError(
                'Invalid plugin_name "{plugin_name}".'.format(
                    plugin_name=plugin_name,
                )
            )
        if plugin_name not in self:
            return
        plugin_type = valid_plugins.get_plugin_type(plugin_name)
        self._base_import = self._base_import_prefix + plugin_type + '.'
        self._current_plugin = plugin_name
        super()._remove_modules(plugin_name)

    def _remove_module(self, module):
        """Remove a module."""
        plugin_path = GUNGAME_PLUGINS_PATH.joinpath(
            valid_plugins.get_plugin_type(self._current_plugin),
            self._current_plugin,
            '__init__.py',
        )
        if plugin_path == sys.modules[module].__file__:
            return
        super()._remove_module(module)

gg_plugin_manager = _GGPluginManager('gungame')
