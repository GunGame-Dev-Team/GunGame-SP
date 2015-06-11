# ../gungame/core/events/__init__.py

"""GunGame custom event functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Importlib
from importlib import import_module

# Site-Package Imports
#   Path
from path import Path

# GunGame Imports
#   Plugins
from gungame.core.plugins.paths import GUNGAME_PLUGIN_PATH
from gungame.core.plugins.valid import valid_plugins


# =============================================================================
# >> CORE CUSTOM EVENT REGISTRATION
# =============================================================================
# Import the included events
for event_file in Path(__file__).parent.joinpath('included').files():
    if event_file.namebase != '__init__':
        import_module('gungame.core.events.included.' + event_file.namebase)


# =============================================================================
# >> SUB-PLUGIN CUSTOM EVENT REGISTRATION
# =============================================================================
for plugin_name in valid_plugins.all:
    plugin_type = valid_plugins.get_plugin_type(plugin_name)
    if GUNGAME_PLUGIN_PATH.joinpath(
            plugin_type, plugin_name, 'custom_events.py').isfile():
        import_module(
            'gungame.plugins.{0}.{1}.custom_events'.format(
                plugin_type, plugin_name))
