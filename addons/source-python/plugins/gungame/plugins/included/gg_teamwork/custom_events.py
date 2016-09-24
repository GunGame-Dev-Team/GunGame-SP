# ../gungame/plugins/included/gg_teamwork/custom_events.py

"""Events used by gg_teamwork."""

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
    'GG_Team_Win',
)


# =============================================================================
# >> CLASSES
# =============================================================================
class GG_Team_Win(CustomEvent):
    """Called during team-based play when a team wins the match."""

    winner = ShortVariable('The team that won the match')
    loser = ShortVariable('The team that lost the match')


# =============================================================================
# >> RESOURCE FILE
# =============================================================================
GGResourceFile(info.name, GG_Team_Win)
