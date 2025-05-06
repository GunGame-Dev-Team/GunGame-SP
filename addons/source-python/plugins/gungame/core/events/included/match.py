# ../gungame/core/events/included/match.py

"""Match based events."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events.custom import CustomEvent
from events.variable import ShortVariable

# GunGame
from ..resource import GGResourceFile

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "GG_Load",
    "GG_Map_End",
    "GG_Start",
    "GG_Unload",
    "GG_Win",
)


# =============================================================================
# >> CLASSES
# =============================================================================
# ruff: noqa: N801
class GG_Win(CustomEvent):
    """Called when a player wins the match."""

    attacker = winner = ShortVariable(
        "The userid of the player that won the match",
    )
    userid = loser = ShortVariable(
        "The userid of that player that caused the winner to win the match",
    )


class GG_Start(CustomEvent):
    """Called when a new match begins."""


class GG_Map_End(CustomEvent):
    """Called when no winner is declared but the map ends."""


class GG_Load(CustomEvent):
    """Called when GunGame finishes loading."""


class GG_Unload(CustomEvent):
    """Called when GunGame is unloading."""


# =============================================================================
# >> RESOURCE FILE
# =============================================================================
GGResourceFile("match", GG_Win, GG_Start, GG_Map_End, GG_Load, GG_Unload)
