# ../gungame/core/events/included/match.py

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Events
from events.custom import CustomEvent
from events.variable import ShortVariable

# GunGame Imports
#   Events
from gungame.core.events.resource import GGResourceFile


# =============================================================================
# >> CLASSES
# =============================================================================
class GG_Win(CustomEvent):
    ''''''

    attacker = winner = ShortVariable(
        'The userid of the player that won the match')
    userid = loser = ShortVariable(
        'The userid of that player that caused the winner to win the match')


class GG_Start(CustomEvent):
    ''''''


class GG_Map_End(CustomEvent):
    ''''''


class GG_Load(CustomEvent):
    ''''''


class GG_Unload(CustomEvent):
    ''''''


# =============================================================================
# >> RESOURCE FILE
# =============================================================================
GGIncludedPlugins = GGResourceFile(
    'match', GG_Win, GG_Start, GG_Map_End, GG_Load, GG_Unload)
