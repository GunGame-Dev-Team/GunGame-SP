# ../gungame/core/status/events.py

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Events
from events import Event

# GunGame Imports
#   Status
from gungame.core.status import GunGameStatus
from gungame.core.status import StatusTypes


# =============================================================================
# >> EVENTS
# =============================================================================
@Event
def gg_win(game_event):
    '''Set match status to inactive when someone has won the match'''
    GunGameStatus.Match = StatusTypes.INACTIVE


@Event
def gg_match_end(game_event):
    '''
        Set match status to inactive when the match has ended without a winner
    '''
    GunGameStatus.Match = StatusTypes.INACTIVE


@Event
def gg_start(game_event):
    '''Set match status to active when the match starts'''
    GunGameStatus.Match = StatusTypes.ACTIVE


@Event
def round_start(game_event):
    '''Set round status to active when the round starts'''
    GunGameStatus.Round = StatusTypes.ACTIVE


@Event
def round_end(game_event):
    '''Set round status to inactive when the round ends'''
    GunGameStatus.Round = StatusTypes.INACTIVE
