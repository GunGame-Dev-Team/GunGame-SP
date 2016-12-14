# ../gungame/plugins/included/gg_knife_steal/custom_events.py

"""Events used by gg_knife_steal."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events.custom import CustomEvent
from events.variable import ByteVariable, ShortVariable

# GunGame
from gungame.core.events.resource import GGResourceFile

# Plugin
from .info import info


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'GG_Knife_Steal',
)


# =============================================================================
# >> CLASSES
# =============================================================================
class GG_Knife_Steal(CustomEvent):
    """Called when a player steals a level by knifing."""

    attacker = leveler = ShortVariable(
        'The userid of the player that stole the level'
    )
    attacker_level = ByteVariable('The new level of the attacker')
    userid = victim = ShortVariable(
        'The userid of the player that had a level stolen'
    )
    userid_level = ByteVariable('The new level of the victim')


# =============================================================================
# >> RESOURCE FILE
# =============================================================================
GGResourceFile(info.name, GG_Knife_Steal)
