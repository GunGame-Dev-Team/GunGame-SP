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
from listeners.tick import Delay, Repeat
from players.entity import Player


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_flashed_players = {}


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_blind')
def _player_blind(game_event):
    """"""
    userid = game_event['userid']
    player = Player.from_userid(userid)
    _cancel_delay(userid)
    _flashed_players[userid] = Delay(
        player.flash_duration,
        _remove_radar_from_player,
        (userid,),
    )


@Event('player_disconnect')
def _player_disconnect(game_event):
    """"""
    _cancel_delay(game_event['userid'])


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
@Repeat
def _remove_radar():
    """"""
    for player in PlayerIter('alive'):
        if player.userid not in _flashed_players:
            _remove_radar_from_player(player.userid)

_remove_radar.start(0.5, execute_on_start=True)


def _remove_radar_from_player(userid):
    """"""
    with suppress(KeyError):
        del _flashed_players[userid]
    player = Player.from_userid(userid)
    player.flash_alpha = 0
    player.flash_duration = time()


def _cancel_delay(userid):
    """"""
    delay = _flashed_players.pop(userid, None)
    if delay is not None:
        delay.cancel()
