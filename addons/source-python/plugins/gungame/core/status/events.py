# ../gungame/core/status/events.py

"""Events used to set GunGame status values."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Events
from events import Event
#   Listeners
from listeners import LevelInit

# GunGame Imports
#   Status
from gungame.core.status import gungame_status
from gungame.core.status import GunGameStatus


# =============================================================================
# >> EVENTS
# =============================================================================
@Event
def gg_win(game_event):
    """Set match status to POST when someone has won the match."""
    gungame_status.match = GunGameStatus.POST


@Event
def gg_map_end(game_event):
    """Set match status to POST when the match has ended without a winner."""
    gungame_status.match = GunGameStatus.POST


@Event
def gg_start(game_event):
    """Set match status to ACTIVE when the match starts."""
    gungame_status.match = GunGameStatus.ACTIVE


@Event
def round_start(game_event):
    """Set round status to ACTIVE when the round starts."""
    gungame_status.round = GunGameStatus.ACTIVE


@Event
def round_end(game_event):
    """Set round status to INACTIVE when the round ends."""
    gungame_status.round = GunGameStatus.INACTIVE


# =============================================================================
# >> LISTENERS
# =============================================================================
@LevelInit
def level_init(mapname):
    """Set match status to INACTIVE when a new map is started."""
    gungame_status.match = GunGameStatus.INACTIVE
