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
from gungame.core.status import GunGameRoundStatus, GunGameStatus
from gungame.core.messages import message_manager
from gungame.core.players.dictionary import player_dictionary


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_eliminated_players = defaultdict(set)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_death')
def _player_death(game_event):
    """Respawn any players the victim killed."""
    if GunGameStatus.ROUND is GunGameRoundStatus.INACTIVE:
        return
    victim = player_dictionary[game_event['userid']]
    Delay(0, _respawn_victims, args=(victim.userid, ))
    attacker = game_event['attacker']
    if attacker in (victim.userid, 0):
        Delay(5, _respawn_player, args=(victim.userid, ))
        victim.chat_message('Elimination:Suicide')
        return
    killer = player_dictionary[attacker]
    if victim.team == killer.team:
        Delay(5, _respawn_player, args=(victim.userid, ))
        victim.chat_message('Elimination:TeamKill')
        return
    # TODO: Test reconnecting to see if players are not respawned
    _eliminated_players[killer.userid].add(victim.userid)
    victim.chat_message(
        'Elimination:Attacker',
        killer.index,
        attacker=killer
    )


@Event('round_start')
def _round_start(game_event):
    """Send the elimination info message."""
    message_manager.chat_message('Elimination:RoundInfo')


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _respawn_victims(userid):
    """Respawn all victim's of the given userid."""
    victims = _eliminated_players.pop(userid, [])
    if not len(victims):
        return
    if GunGameStatus.ROUND is GunGameRoundStatus.INACTIVE:
        return
    players = list()
    for victim in victims:
        player = player_dictionary.get(victim)
        if player is None:
            continue
        if player.team == 1:
            continue
        players.append(player)
        player.spawn()
    if players:
        message_manager.chat_message(
            'Elimination:Respawning', players[0].index,
            player='\x01, \x03'.join(
                map(
                    attrgetter('name'),
                    players
                )
            )
        )


def _respawn_player(userid):
    """Respawn the given userid after validation."""
    if GunGameStatus.ROUND is GunGameRoundStatus.INACTIVE:
        return
    player = player_dictionary.get(userid)
    if player is not None:
        player.spawn()
