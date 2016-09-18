# ../gungame/plugins/included/gg_multi_level/custom_events.py

"""Events used by gg_multi_level."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events.custom import CustomEvent
from events.variable import ShortVariable

# GunGame
from gungame.core.events.resource import GGResourceFile

# Plugin
from .info import info


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'GG_Multi_Level',
)


# =============================================================================
# >> CLASSES
# =============================================================================
class GG_Multi_Level(CustomEvent):
    """Called when a player achieves a multi-level bonus."""

    userid = leveler = ShortVariable(
        'The userid of the player that multi-leveled')


# =============================================================================
# >> RESOURCE FILE
# =============================================================================
GGResourceFile(info.name, GG_Multi_Level)
