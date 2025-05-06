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
from gungame.info import info

from ..plugins.valid import valid_plugins

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "gungame_player_settings",
    "register_player_settings",
)


# =============================================================================
# >> SETTINGS
# =============================================================================
gungame_player_settings = PlayerSettings(info.name, "gg", info.verbose_name)


# =============================================================================
# >> SUB-PLUGIN PLAYER SETTINGS REGISTRATION
# =============================================================================
def register_player_settings():
    """Register all player settings."""
    for plugin_name in valid_plugins.all:
        plugin_path = valid_plugins.get_plugin_path(plugin_name)
        plugin_type = str(plugin_path.parent.stem)
        settings_path = plugin_path / "settings.py"
        if settings_path.is_file():
            import_module(
                f"gungame.plugins.{plugin_type}.{plugin_name}.settings",
            )
