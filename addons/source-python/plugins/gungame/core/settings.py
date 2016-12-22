# ../gungame/core/settings.py

"""Provides player settings for GunGame."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from importlib import import_module

# Source.Python
from settings.player import PlayerSettings

# GunGame
from gungame.info import info
from gungame.core.paths import GUNGAME_PLUGINS_PATH
from gungame.core.plugins.valid import valid_plugins


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
gungame_player_settings = PlayerSettings(info.name, 'gg')


# =============================================================================
# >> SUB-PLUGIN PLAYER SETTINGS REGISTRATION
# =============================================================================
def register_player_settings():
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
