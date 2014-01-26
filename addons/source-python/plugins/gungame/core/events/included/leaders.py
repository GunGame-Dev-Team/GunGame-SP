# ../gungame/core/events/included/leaders.py

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Events
from events.custom import CustomEvent
from events.variable import ByteVariable
from events.variable import ShortVariable
from events.variable import StringVariable

# GunGame Imports
#   Events
from gungame.core.events.resource import GGResourceFile


# =============================================================================
# >> CLASSES
# =============================================================================
class GG_New_Leader(CustomEvent):
    ''''''

    userid = leveler = ShortVariable(
        'The userid of the player that became the new leader')
    leaders = StringVariable(
        'String of current leaders separated by "," e.g. "2,7,9"')
    old_leaders = StringVariable(
        'String of the old leaders separated by "," e.g. "2,7,9"')
    leader_level = ByteVariable("The current leader's level")


class GG_Tied_Leader(CustomEvent):
    ''''''

    userid = leveler = ShortVariable(
        'The userid of the player that tied the leader(s)')
    leaders = StringVariable(
        'String of current leaders separated by "," e.g. "2,7,9"')
    old_leaders = StringVariable(
        'String of the old leaders separated by "," e.g. "2,7,9"')
    leader_level = ByteVariable("The current leader's level")


class GG_Leader_LostLevel(CustomEvent):
    ''''''

    userid = leveler = ShortVariable(
        'The userid of the leader that lost a level')
    leaders = StringVariable(
        'String of current leaders separated by "," e.g. "2,7,9"')
    old_leaders = StringVariable(
        'String of the old leaders separated by "," e.g. "2,7,9"')
    leader_level = ByteVariable("The current leader's level")


class GG_Leader_Disconnect(CustomEvent):
    ''''''

    userid = ShortVariable('The userid of the leader that disconnected')
    leaders = StringVariable(
        'String of current leaders separated by "," e.g. "2,7,9"')
    old_leaders = StringVariable(
        'String of the old leaders separated by "," e.g. "2,7,9"')
    leader_level = ByteVariable("The current leader's level")


# =============================================================================
# >> RESOURCE FILE
# =============================================================================
GGIncludedPlugins = GGResourceFile(
    'leaders', GG_New_Leader, GG_Tied_Leader,
    GG_Leader_LostLevel, GG_Leader_Disconnect)
