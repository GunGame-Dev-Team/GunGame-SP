# ../gungame/plugins/included/gg_ffa/games/cstrike.py

"""CS:S specific functionality for gg_ffa."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from contextlib import suppress
from time import time

# Source.Python
from events import Event
from filters.players import PlayerIter
from listeners import OnLevelShutdown
from listeners.tick import Delay, Repeat
from players.entity import Player

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_flashed_players = {}


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event("player_blind")
def _player_blind(game_event):
    """Add the player to a dictionary of flashed players to not remove HUD."""
    userid = game_event["userid"]
    player = Player.from_userid(userid)
    _cancel_delay(userid)
    _flashed_players[userid] = Delay(
        delay=player.flash_duration,
        callback=_remove_radar_from_player,
        args=(userid,),
        cancel_on_level_end=True,
    )


@Event("player_disconnect")
def _player_disconnect(game_event):
    """Cancel the player's Delay (if it is ongoing)."""
    _cancel_delay(game_event["userid"])


# =============================================================================
# >> LISTENERS
# =============================================================================
@OnLevelShutdown
def _level_shutdown():
    """Clear the flash dictionary."""
    _flashed_players.clear()


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
@Repeat
def _remove_radar():
    """Remove the radar from all players every half second."""
    for player in PlayerIter("alive"):
        if player.userid not in _flashed_players:
            _remove_radar_from_player(player.userid)


def _remove_radar_from_player(userid):
    """Remove the player's radar."""
    with suppress(KeyError):
        del _flashed_players[userid]
    player = Player.from_userid(userid)
    player.flash_alpha = 0
    player.flash_duration = time()


def _cancel_delay(userid):
    """Cancel the given player's Delay."""
    delay = _flashed_players.pop(userid, None)
    if delay is not None:
        delay.cancel()


_remove_radar.start(0.5, execute_on_start=True)
