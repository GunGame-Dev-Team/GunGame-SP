# ../gungame/core/status/events.py

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Events
from events import Event

# GunGame Imports
#   Status
from gungame.core.status import gungame_status
from gungame.core.status import GunGameStatusTypes


# =============================================================================
# >> EVENTS
# =============================================================================
@Event
def gg_win(game_event):
    """Set match status to inactive when someone has won the match"""
    gungame_status.match = GunGameStatusTypes.INACTIVE


@Event
def gg_match_end(game_event):
    """
        Set match status to inactive when the match has ended without a winner
    """
    gungame_status.match = GunGameStatusTypes.INACTIVE


@Event
def gg_start(game_event):
    """Set match status to active when the match starts"""
    gungame_status.match = GunGameStatusTypes.ACTIVE


@Event
def round_start(game_event):
    """Set round status to active when the round starts"""
    gungame_status.round = GunGameStatusTypes.ACTIVE


@Event
def round_end(game_event):
    """Set round status to inactive when the round ends"""
    gungame_status.round = GunGameStatusTypes.INACTIVE
