# ../gungame/plugins/included/gg_teamplay/custom_events.py

"""Events used by gg_teamplay."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events.custom import CustomEvent
from events.variable import ByteVariable, ShortVariable, StringVariable

# GunGame
from gungame.core.events.resource import GGResourceFile

# Plugin
from .info import info


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'GG_Team_Level_Up',
    'GG_Team_Win',
)


# =============================================================================
# >> CLASSES
# =============================================================================
class GG_Team_Level_Up(CustomEvent):
    """Called during team-based play when a team levels up."""

    team = ShortVariable('The team that leveled up')
    old_level = ByteVariable('The old level of the team that leveled up')
    new_level = ByteVariable('The new level of the team that leveled up')
    style = StringVariable('The style of teamplay match')


class GG_Team_Win(CustomEvent):
    """Called during team-based play when a team wins the match."""

    winner = ShortVariable('The team that won the match')
    loser = ShortVariable('The team that lost the match')
    style = StringVariable('The style of teamplay match')


# =============================================================================
# >> RESOURCE FILE
# =============================================================================
GGResourceFile(info.name, GG_Team_Level_Up, GG_Team_Win)
