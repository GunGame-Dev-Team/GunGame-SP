# ../gungame/core/events/included/leveling.py

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
class GG_LevelUp(CustomEvent):
    ''''''

    attacker = leveler = ShortVariable(
        'The userid of the player that leveled up')
    userid = victim = ShortVariable(
        'The userid of the victim that caused the levelup')
    old_level = ByteVariable('The old level of the player that leveled up')
    new_level = ByteVariable('The new level of the player that leveled up')
    reason = StringVariable('The reason for the levelup')


class GG_LevelDown(CustomEvent):
    ''''''

    userid = leveler = ShortVariable(
        'The userid of the player that leveled down')
    old_level = ByteVariable('The old level of the player that leveled down')
    new_level = ByteVariable('The new level of the player that leveled down')
    reason = StringVariable('The reason for the leveldown')


# =============================================================================
# >> RESOURCE FILE
# =============================================================================
GGIncludedPlugins = GGResourceFile('leveling', GG_LevelUp, GG_LevelDown)
