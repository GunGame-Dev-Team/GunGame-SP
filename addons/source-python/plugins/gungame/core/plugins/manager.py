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
from ..events.included.plugins import GG_Plugin_Loaded, GG_Plugin_Unloaded
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
    _base_import = ''
    translations = None

    def set_base_import(self, value):
        """Set the base import for other functionality."""
        if value not in ('included', 'custom'):
            raise ValueError(
                f'Value must be "included" or "custom" not "{value}".'
            )
        self._base_import = self._base_import_prefix + value + '.'

    @property
    def is_team_game(self):
        """Return whether or not the current match is a team game."""
        return any(team_levels.values())

    def load(self, plugin_name):
        """Load the given plugin."""
        self.logger.log_message(
            self.prefix + self.translations[
                'Loading'
            ].get_string(plugin=plugin_name)
        )
        super().load(plugin_name)

        # Was the plugin unable to be loaded?
        if plugin_name not in self:
            self.logger.log_message(
                self.prefix + self.translations[
                    'Unable to Load'
                ].get_string(plugin=plugin_name)
            )
            return

        self.logger.log_message(
            self.prefix + self.translations[
                'Successful Load'
            ].get_string(plugin=plugin_name)
        )
        with GG_Plugin_Loaded() as event:
            event.plugin = plugin_name
            event.plugin_type = valid_plugins.get_plugin_type(plugin_name)

    def unload(self, plugin_name, indent=0):
        """Unload the given plugin."""
        self.logger.log_message(
            ' ' * indent + self.prefix + self.translations[
                'Unloading'
            ].get_string(plugin=plugin_name)
        )
        super().unload(plugin_name)
        if plugin_name in self:
            return

        self.logger.log_message(
            ' ' * indent + self.prefix + self.translations[
                'Successful Unload'
            ].get_string(plugin=plugin_name)
        )
        with GG_Plugin_Unloaded() as event:
            event.plugin = plugin_name
            event.plugin_type = valid_plugins.get_plugin_type(
                plugin_name=plugin_name,
            )

    def _remove_modules(self, plugin_name):
        """Remove a plugin and all its modules."""
        if plugin_name not in valid_plugins.all:
            raise ValueError(f'Invalid plugin_name "{plugin_name}".')
        if plugin_name not in self:
            return
        plugin_type = valid_plugins.get_plugin_type(plugin_name)
        self._base_import = self._base_import_prefix + plugin_type + '.'
        super()._remove_modules(plugin_name)

    @staticmethod
    def _is_related_module(base_name, module_to_check):
        """Check if a plugin's base name is related to a module name."""
        if module_to_check.split('.')[~0] in (
            'commands', 'configuration', 'custom_events', 'info', 'rules',
            'settings',
        ):
            return False
        if base_name == module_to_check:
            return False
        return PluginManager._is_related_module(base_name, module_to_check)

gg_plugin_manager = _GGPluginManager('gungame')
