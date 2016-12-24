# ../gungame/plugins/included/gg_teamwork/gg_teamwork.py

"""Plugin that levels players up individually to win as a team."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from colors import BLUE, RED, WHITE
from cvars import ConVar
from entities.entity import Entity
from events import Event
from events.hooks import EventAction, PreEvent
from listeners import OnLevelInit
from listeners.tick import Delay
from players.teams import teams_by_number

# GunGame
from gungame.core.config.misc import dynamic_chat_time
from gungame.core.messages import message_manager
from gungame.core.players.dictionary import player_dictionary
from gungame.core.sounds.manager import sound_manager
from gungame.core.status import GunGameMatchStatus, GunGameStatus
from gungame.core.teams import team_names
from gungame.core.weapons.manager import weapon_order_manager

# Plugin
from .configuration import join_team_level
from .custom_events import GG_Team_Win


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    message_manager.hook_prefix('Leader:')


# =============================================================================
# >> CLASSES
# =============================================================================
class _TeamManager(dict):
    def clear(self):
        for team_number in self:
            self[team_number].reset_values()


class _TeamManagement(object):

    def __init__(self, number, alias):
        self.number = number
        self.alias = alias
        self.level = 1
        self.name = team_names[self.number]
        self._leader = None
        self.leader_userid = None

    @property
    def index(self):
        return self.leader.index if self.leader is not None else 0

    @property
    def leader(self):
        return self._leader

    @leader.setter
    def leader(self, player):
        current = self._leader
        self._leader = player
        self.leader_userid = None if player is None else player.userid
        if current is None or player is None:
            return
        if current.level < player.level or current.userid == player.userid:
            message_manager.chat_message(
                message='TeamWork:Leader:Increase',
                index=self.index,
                player=player.name,
                team_name=self.name,
                level=self.leader_level,
            )

    @property
    def leader_level(self):
        return None if self.leader is None else self.leader.level

    @property
    def color(self):
        return RED if self.number == 2 else BLUE

    def reset_values(self):
        self.leader = None

    def set_team_player_levels(self):
        if self.leader_level is None:
            self.find_team_leader()
        self.level = self.leader_level
        if self.level is None:
            return
        for player in player_dictionary.values():
            if player.team != self.number:
                continue
            if player.level == self.level:
                continue
            player.level = self.level
            player.multi_kill = 0

    def set_joining_player_level(self, player):
        player.level = self.level if join_team_level.get_int() else 1

    def find_team_leader(self, leveler=None, old_level=None, disconnect=False):
        team_players = {
            player.level: player for player in player_dictionary.values()
            if player.team == self.number
        }
        if not team_players:
            self.leader = None
            return
        self.leader = team_players[max(team_players.keys())]

        if disconnect:
            message_manager.chat_message(
                message='TeamWork:Leader:Disconnect',
                index=self.index,
                team_name=self.name,
                level=self.leader_level,
            )
            return

        if leveler is None or old_level is None:
            return

        if self.leader_level is not None and self.leader_level < old_level:
            message_manager.chat_message(
                message='TeamWork:Leader:Decrease',
                index=self.index,
                player=leveler.name,
                team_name=self.name,
                level=self.leader_level,
            )

    def send_level_message(self):
        if self.leader_level is None:
            return
        message_manager.chat_message(
            message='TeamWork:TeamLevel',
            index=self.index,
            team_name=self.name,
            level=self.leader_level,
            weapon=weapon_order_manager.active[self.leader_level].weapon,
        )

_team_manager = _TeamManager({
    number: _TeamManagement(number, alias)
    for number, alias in teams_by_number.items()
    if alias not in ('un', 'spec')
})


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_team')
def _check_team_leaders(game_event):
    userid = game_event['userid']
    old_team_number = game_event['oldteam']

    old_team = _team_manager.get(old_team_number)
    if old_team and old_team.leader_userid == userid:
        old_team.find_team_leader(disconnect=True)

    new_team = _team_manager.get(game_event['team'])
    if not new_team:
        return

    if not old_team_number:
        new_team.set_joining_player_level(player_dictionary[userid])

    else:
        new_team.find_team_leader()


@Event('round_start')
def _send_level_messages(game_event):
    for team in _team_manager.values():
        team.send_level_message()


@Event('round_end')
def _sync_player_levels(game_event):
    for team in _team_manager.values():
        team.set_team_player_levels()


# =============================================================================
# >> GUNGAME EVENTS
# =============================================================================
@Event('gg_start')
@OnLevelInit
def _clear_team_dictionary(game_event=None):
    _team_manager.clear()


@Event('gg_level_up')
def _level_up(game_event):
    player = player_dictionary[game_event['leveler']]
    team = _team_manager[player.team]
    if (
        team.leader_userid in (None, player.userid) or
        team.leader_level < game_event['new_level']
    ):
        team.leader = player


@Event('gg_level_down')
def _check_team_decrease(game_event):
    player = player_dictionary[game_event['leveler']]
    team = _team_manager[player.team]
    if team.leader.userid == player.userid:
        team.find_team_leader(player, game_event['old_level'])


@Event('gg_team_win')
def _end_match(game_event):
    # Set the match status
    GunGameStatus.MATCH = GunGameMatchStatus.POST

    # Get the winning team information
    winning_team = _team_manager[game_event['winner']]

    # Send the winner messages
    message_manager.chat_message(
        index=winning_team.index,
        message='TeamWork:Winner:Long',
        team_name=winning_team.name,
    )
    for second in range(4):
        Delay(
            second,
            message_manager.center_message,
            kwargs={
                'message': 'TeamWork:Winner:Short',
                'team_name': winning_team.name,
            }
        )
    color = {2: RED, 3: BLUE}.get(winning_team, WHITE)
    message_manager.top_message(
        message='TeamWork:Winner:Short',
        color=color,
        team_name=winning_team.name,
    )

    # Play the winner sound
    winner_sound = sound_manager.play_sound('winner')

    # Set the dynamic chat time, if needed
    if dynamic_chat_time.get_bool():
        ConVar('mp_chattime').set_float(winner_sound.duration)

    # End the match to move to the next map
    entity = Entity.find_or_create('game_end')
    entity.end_game()

    # Reset the teams
    _clear_team_dictionary()


# =============================================================================
# >> EVENT HOOKS
# =============================================================================
@PreEvent('gg_win')
def pre_gg_win(game_event):
    team_number = player_dictionary[game_event['winner']].team
    Delay(
        delay=0,
        callback=_fire_win_event,
        args=(
            team_number,
        ),
    )
    return EventAction.BLOCK


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _fire_win_event(team_number):
    with GG_Team_Win() as event:
        event.winner = team_number
        event.loser = 5 - team_number
