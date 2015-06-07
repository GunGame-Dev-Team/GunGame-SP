# ../gungame/core/events/included/voting.py

"""Voting based events."""

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

    """Called when a vote has started."""

    vote_type = StringVariable('The type of vote')


class GG_Vote_End(CustomEvent):

    """Called when a vote ends."""

    winner = StringVariable('The winning choice')


class GG_Vote_Submit(CustomEvent):

    """Called each time a vote is submitted."""

    userid = voter = ShortVariable('The userid of the player that voted')
    choice = StringVariable('The choice submitted by the player')


class GG_Vote_Canceled(CustomEvent):

    """Called when a vote ends by being canceled."""

    reason = StringVariable('The reason the vote was canceled')


# =============================================================================
# >> RESOURCE FILE
# =============================================================================
GGIncludedPlugins = GGResourceFile(
    'voting', GG_Vote_Start, GG_Vote_End, GG_Vote_Submit, GG_Vote_Canceled)
