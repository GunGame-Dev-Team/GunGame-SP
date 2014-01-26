# ../gungame/core/events/included/voting.py

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Events
from events.custom import CustomEvent
from events.variable import ShortVariable
from events.variable import StringVariable

# GunGame Imports
#   Events
from gungame.core.events.resource import GGResourceFile


# =============================================================================
# >> CLASSES
# =============================================================================
class GG_Vote_Start(CustomEvent):
    ''''''


class GG_Vote_End(CustomEvent):
    ''''''


class GG_Vote_Submit(CustomEvent):
    ''''''

    userid = voter = ShortVariable('The userid of the player that voted')
    choice = StringVariable('The choice submitted by the player')


class GG_Vote_Canceled(CustomEvent):
    ''''''


# =============================================================================
# >> RESOURCE FILE
# =============================================================================
GGIncludedPlugins = GGResourceFile(
    'voting', GG_Vote_Start, GG_Vote_End, GG_Vote_Submit, GG_Vote_Canceled)
