# ../gungame/core/events/included/leveling.py

"""Leveling based events."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events.custom import CustomEvent
from events.variable import ByteVariable, ShortVariable, StringVariable

# GunGame
from ..resource import GGResourceFile


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'GG_Level_Down',
    'GG_Level_Up',
)


# =============================================================================
# >> CLASSES
# =============================================================================
class GG_Level_Up(CustomEvent):
    """Called when a player levels up."""

    attacker = leveler = ShortVariable(
        'The userid of the player that leveled up'
    )
    userid = victim = ShortVariable(
        'The userid of the victim that caused the level-up'
    )
    old_level = ByteVariable('The old level of the player that leveled up')
    new_level = ByteVariable('The new level of the player that leveled up')
    reason = StringVariable('The reason for the level-up')


class GG_Level_Down(CustomEvent):
    """Called when a player loses a level."""

    userid = leveler = ShortVariable(
        'The userid of the player that leveled down'
    )
    attacker = ShortVariable(
        'The userid of the player that caused the level down'
    )
    old_level = ByteVariable('The old level of the player that leveled down')
    new_level = ByteVariable('The new level of the player that leveled down')
    reason = StringVariable('The reason for the level-down')


# =============================================================================
# >> RESOURCE FILE
# =============================================================================
GGResourceFile('leveling', GG_Level_Up, GG_Level_Down)
