# ../gungame/core/settings/__init__.py

"""Provides player settings for GunGame."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from importlib import import_module

# Source.Python
from settings.player import PlayerSettings

# GunGame
from ..paths import GUNGAME_PLUGINS_PATH
from ..plugins.valid import valid_plugins
from gungame.info import info


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'gungame_player_settings',
    'register_player_settings',
)


# =============================================================================
# >> SETTINGS
# =============================================================================
gungame_player_settings = PlayerSettings(info.name, 'gg', info.verbose_name)


# =============================================================================
# >> SUB-PLUGIN PLAYER SETTINGS REGISTRATION
# =============================================================================
def register_player_settings():
    """Register all player settings."""
    for plugin_name in valid_plugins.all:
        plugin_type = valid_plugins.get_plugin_type(plugin_name)
        if GUNGAME_PLUGINS_PATH.joinpath(
            plugin_type, plugin_name, 'settings.py',
        ).isfile():
            import_module(
                'gungame.plugins.{plugin_type}.{plugin_name}.settings'.format(
                    plugin_type=plugin_type,
                    plugin_name=plugin_name,
                )
            )
