# ../gungame/core/events/included/plugins.py

"""Sub-plugin based events."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events.custom import CustomEvent
from events.variable import StringVariable

# GunGame
from ..resource import GGResourceFile

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "GG_Plugin_Loaded",
    "GG_Plugin_Unloaded",
)


# =============================================================================
# >> CLASSES
# =============================================================================
# ruff: noqa: N801
class GG_Plugin_Loaded(CustomEvent):
    """Called when a GunGame sub-plugin is loaded."""

    plugin = StringVariable("The name of the plugin that was loaded")
    plugin_type = StringVariable("The type of plugin that was loaded")


class GG_Plugin_Unloaded(CustomEvent):
    """Called when a GunGame sub-plugin is unloaded."""

    plugin = StringVariable("The name of the plugin that was unloaded")
    plugin_type = StringVariable("The type of plugin that was unloaded")


# =============================================================================
# >> RESOURCE FILE
# =============================================================================
GGResourceFile("plugins", GG_Plugin_Loaded, GG_Plugin_Unloaded)
