# ../gungame/plugins/included/gg_elimination/gg_elimination.py

"""Plugin that respawns players when their killer is killed."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import defaultdict
from operator import attrgetter

# Source.Python
from events import Event
from listeners.tick import Delay

# GunGame
from gungame.core.messages.manager import message_manager
from gungame.core.players.dictionary import player_dictionary
from gungame.core.status import (
    GunGameMatchStatus,
    GunGameRoundStatus,
    GunGameStatus,
)

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
eliminated_players = defaultdict(set)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event("player_death")
def _player_death(game_event):
    """Respawn any players the victim killed."""
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    if GunGameStatus.ROUND is GunGameRoundStatus.INACTIVE:
        return

    victim = player_dictionary[game_event["userid"]]
    Delay(
        delay=0,
        callback=_respawn_victims,
        args=(victim.userid,),
    )
    attacker = game_event["attacker"]
    if attacker in (victim.userid, 0):
        Delay(
            delay=5,
            callback=_respawn_player,
            args=(victim.userid,),
            cancel_on_level_end=True,
        )
        victim.chat_message("Elimination:Suicide")
        return
    killer = player_dictionary[attacker]
    if victim.team_index == killer.team_index:
        Delay(
            delay=5,
            callback=_respawn_player,
            args=(victim.userid,),
            cancel_on_level_end=True,
        )
        victim.chat_message("Elimination:TeamKill")
        return
    eliminated_players[killer.userid].add(victim.userid)
    victim.chat_message(
        "Elimination:Attacker",
        killer.index,
        attacker=killer,
    )


@Event("round_start")
def _round_start(game_event):
    """Send the elimination info message."""
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    message_manager.chat_message("Elimination:RoundInfo")


@Event("round_end")
def _round_end(game_event):
    """Clear the dictionary."""
    eliminated_players.clear()


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _respawn_victims(userid):
    """Respawn all victim's of the given userid."""
    victims = eliminated_players.pop(userid, [])
    if not victims:
        return
    if GunGameStatus.ROUND is GunGameRoundStatus.INACTIVE:
        return
    players = []
    for victim in victims:
        player = player_dictionary.get(victim)
        if player is None:
            continue
        if player.team_index == 1:
            continue
        players.append(player)
        player.spawn()
    if players:
        message_manager.chat_message(
            "Elimination:Respawning", players[0].index,
            player="\x01, \x03".join(
                map(
                    attrgetter("name"),
                    players,
                ),
            ),
        )


def _respawn_player(userid):
    """Respawn the given userid after validation."""
    if GunGameStatus.ROUND is GunGameRoundStatus.INACTIVE:
        return
    player = player_dictionary.get(userid)
    if player is not None:
        player.spawn()
