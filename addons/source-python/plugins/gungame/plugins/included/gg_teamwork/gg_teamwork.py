# ../gungame/plugins/included/gg_teamwork/gg_teamwork.py

"""Plugin that levels players up individually to win as a team."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from colors import BLUE, RED
from entities.entity import Entity
from events import Event
from events.hooks import EventAction, PreEvent
from listeners import OnLevelInit
from players.teams import teams_by_number

# GunGame
from gungame.core.players.dictionary import player_dictionary

# Plugin
from .custom_events import GG_Team_Win


# =============================================================================
# >> CLASSES
# =============================================================================
class _TeamManager(dict):
    def clear(self):
        for team_number in self:
            self[team_number].reset_values()


class _TeamManagement(object):
    level = 1
    leader = None

    def __init__(self, number, alias):
        self.number = number
        self.alias = alias

    @property
    def index(self):
        return 1

    @property
    def leader_level(self):
        return 1

    @property
    def color(self):
        return RED if self.number == 2 else BLUE

    def reset_values(self):
        self.level = 1
        self.leader = None

    def set_all_player_levels(self):
        pass

    def set_joining_player_level(self):
        pass

    def check_old_leader(self):
        pass

    def find_team_leader(self):
        pass

    def send_level_message(self):
        pass

    def send_winner_messages(self):
        pass

    def send_message_to_all(self, message, **tokens):
        pass

_team_manager = _TeamManager({
    number: _TeamManagement(number, alias)
    for number, alias in teams_by_number.items()
    if alias not in ('un', 'spec')
})


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('')
def something():
    pass


@Event('gg_start', 'gg_team_win')
@OnLevelInit
def _clear_team_dictionary(game_event=None):
    # TODO: clear team dictionary
    pass


# =============================================================================
# >> GUNGAME EVENTS
# =============================================================================
@Event('gg_team_win')
def _end_match(game_event):
    # TODO: send winner messages
    # TODO: play winner sound
    Entity.find_or_create('game_end').end_game()


@Event('gg_level_up')
def _check_team_increase(game_event):
    # TODO: check to see if player increased team's level
    player = player_dictionary[game_event['leveler']]


@Event('gg_level_down')
def _check_team_decrease(game_event):
    # TODO: check to see if player decreased team's level
    player = player_dictionary[game_event['leveler']]


# =============================================================================
# >> EVENT HOOKS
# =============================================================================
@PreEvent('gg_win')
def pre_gg_win(game_event):
    winning_team = player_dictionary[game_event['winner']].team
    with GG_Team_Win() as event:
        event.winner = winning_team,
        event.loser = 5 - winning_team
    return EventAction.BLOCK
