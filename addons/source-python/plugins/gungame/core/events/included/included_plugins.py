# ../gungame/core/events/included/included_plugins.py

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Events
from events.custom import CustomEvent
from events.variable import ByteVariable
from events.variable import ShortVariable

# GunGame Imports
#   Events
from gungame.core.events.resource import GGResourceFile


# =============================================================================
# >> CLASSES
# =============================================================================
class GG_Knife_Steal(CustomEvent):
    ''''''

    attacker = leveler = ShortVariable(
        'The userid of the player that stole the level')
    attacker_level = ByteVariable('The new level of the attacker')
    userid = victim = ShortVariable(
        'The userid of the player that had a level stolen')
    userid_level = ByteVariable('The new level of the victim')


class GG_Multi_Level(CustomEvent):
    ''''''

    userid = leveler = ShortVariable(
        'The userid of the player that multi-leveled')


class GG_Team_Levelup(CustomEvent):
    ''''''

    team = ShortVariable('The team that leveled up')
    old_level = ByteVariable('The old level of the team that leveled up')
    new_level = ByteVariable('The new level of the team that leveled up')


class GG_Team_Win(CustomEvent):
    ''''''

    winner = ShortVariable('The team that won the match')
    loser = ShortVariable('The team that lost the match')


# =============================================================================
# >> RESOURCE FILE
# =============================================================================
GGIncludedPlugins = GGResourceFile(
    'included_plugins', GG_Knife_Steal,
    GG_Multi_Level, GG_Team_Levelup, GG_Team_Win)
