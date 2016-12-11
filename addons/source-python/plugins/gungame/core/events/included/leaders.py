# ../gungame/core/events/included/leaders.py

"""Leader based events."""

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
    'GG_Leader_Disconnect',
    'GG_Leader_Lost_Level',
    'GG_New_Leader',
    'GG_Tied_Leader',
)


# =============================================================================
# >> CLASSES
# =============================================================================
class GG_New_Leader(CustomEvent):
    """Called when a player becomes the new leader."""

    userid = leveler = ShortVariable(
        'The userid of the player that became the new leader'
    )
    old_leaders = StringVariable(
        'String of the old leaders separated by "," e.g. "2,7,9"'
    )
    old_level = ByteVariable('The old leader level')
    leaders = StringVariable(
        'String of current leaders separated by "," e.g. "2,7,9"'
    )
    leader_level = ByteVariable("The current leader's level")


class GG_Tied_Leader(CustomEvent):
    """Called when a player ties the leader."""

    userid = leveler = ShortVariable(
        'The userid of the player that tied the leader(s)'
    )
    old_leaders = StringVariable(
        'String of the old leaders separated by "," e.g. "2,7,9"'
    )
    leaders = StringVariable(
        'String of current leaders separated by "," e.g. "2,7,9"'
    )
    leader_level = ByteVariable("The current leader's level")


class GG_Leader_Lost_Level(CustomEvent):
    """Called when the leader loses a level."""

    userid = leveler = ShortVariable(
        'The userid of the leader that lost a level'
    )
    old_leaders = StringVariable(
        'String of the old leaders separated by "," e.g. "2,7,9"'
    )
    old_level = ByteVariable('The old leader level')
    leaders = StringVariable(
        'String of current leaders separated by "," e.g. "2,7,9"'
    )
    leader_level = ByteVariable("The current leader's level")


class GG_Leader_Disconnect(CustomEvent):
    """Called when the leader disconnects from the server."""

    userid = ShortVariable('The userid of the leader that disconnected')
    old_leaders = StringVariable(
        'String of the old leaders separated by "," e.g. "2,7,9"')
    old_level = ByteVariable('The old leader level')
    leaders = StringVariable(
        'String of current leaders separated by "," e.g. "2,7,9"')
    leader_level = ByteVariable("The current leader's level")


# =============================================================================
# >> RESOURCE FILE
# =============================================================================
GGResourceFile(
    'leaders', GG_New_Leader, GG_Tied_Leader,
    GG_Leader_Lost_Level, GG_Leader_Disconnect,
)
