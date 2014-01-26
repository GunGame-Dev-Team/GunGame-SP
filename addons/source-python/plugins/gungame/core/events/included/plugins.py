# ../gungame/core/events/included/plugins.py

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Events
from events.custom import CustomEvent
from events.variable import StringVariable

# GunGame Imports
#   Events
from gungame.core.events.resource import GGResourceFile


# =============================================================================
# >> CLASSES
# =============================================================================
class GG_Plugin_Loaded(CustomEvent):
    ''''''

    plugin = StringVariable('The name of the plugin that was loaded')
    type = StringVariable('The type of plugin that was loaded')


class GG_Plugin_Unloaded(CustomEvent):
    ''''''

    plugin = StringVariable('The name of the plugin that was unloaded')
    type = StringVariable('The type of plugin that was unloaded')


# =============================================================================
# >> RESOURCE FILE
# =============================================================================
GGIncludedPlugins = GGResourceFile(
    'plugins', GG_Plugin_Loaded, GG_Plugin_Unloaded)
