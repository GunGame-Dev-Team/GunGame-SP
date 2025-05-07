# ../gungame/plugins/included/gg_ffa/gg_ffa.py

"""Plugin that allows FreeForAll gameplay."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from contextlib import suppress
from time import time

# Source.Python
from core import GAME_NAME
from entities import TakeDamageInfo
from entities.entity import Entity
from entities.hooks import EntityCondition, EntityPostHook, EntityPreHook
from events import Event
from filters.players import PlayerIter
from listeners import OnLevelShutdown
from listeners.tick import Delay, Repeat
from memory import make_object
from memory.hooks import use_pre_registers
from players.entity import Player

# GunGame
from gungame.core.status import GunGameMatchStatus, GunGameStatus

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_take_damage_dict = {}
_flashed_players = {}


# =============================================================================
# >> HOOKED FUNCTIONS
# =============================================================================
@EntityPreHook(EntityCondition.is_bot_player, "on_take_damage")
@EntityPreHook(EntityCondition.is_human_player, "on_take_damage")
def _pre_take_damage(stack_data):
    """Change the victim's team if they are on the attacker's team."""
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    take_damage_info = make_object(TakeDamageInfo, stack_data[1])
    attacker = Entity(take_damage_info.attacker)
    if attacker.classname != "player":
        return

    victim = make_object(Entity, stack_data[0])
    if victim.team_index != attacker.team_index:
        return

    address = stack_data[0].address
    if address in _take_damage_dict:
        return

    _take_damage_dict[address] = (victim.index, victim.team_index)

    # Change the player's team by using the m_iTeamNum property
    victim.team_index = 5 - victim.team_index


@EntityPostHook(EntityCondition.is_bot_player, "on_take_damage")
@EntityPostHook(EntityCondition.is_human_player, "on_take_damage")
def _post_take_damage(stack_data, return_value):
    """Revert the victim's team if necessary."""
    with use_pre_registers(stack_data):
        address = stack_data[0].address

    if address not in _take_damage_dict:
        return

    index, team = _take_damage_dict.pop(address)
    Entity(index).team_index = team


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
