# ../gungame/core/plugins/manager.py

"""Provides a class used to load/unload sub-plugins."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from plugins.manager import PluginManager

# GunGame
from . import gg_plugins_logger
from .valid import valid_plugins
from ..events.included.plugins import GG_Plugin_Unloaded
from ..teams import team_levels


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    '_GGPluginManager',
    'gg_plugin_manager',
    'gg_plugins_manager_logger',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_plugins_manager_logger = gg_plugins_logger.manager


# =============================================================================
# >> CLASSES
# =============================================================================
class _GGPluginManager(PluginManager):
    """The GunGame plugin manager class."""

    prefix = ''
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

    @property
    def is_team_game(self):
        return any(team_levels.values())

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

    @staticmethod
    def _is_related_module(base_name, module):
        """Check if a plugin's base name is related to a module name."""
        if module.split('.')[~0] in (
            'configuration', 'custom_events', 'info', 'rules', 'settings',
        ):
            return False
        return PluginManager._is_related_module(base_name, module)

gg_plugin_manager = _GGPluginManager('gungame')
