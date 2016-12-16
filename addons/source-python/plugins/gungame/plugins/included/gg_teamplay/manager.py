# ../gungame/plugins/included/gg_teamplay/manager.py

"""Teamplay management."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events import Event

# GunGame
from gungame.core.messages import message_manager
from gungame.core.players.dictionary import player_dictionary
from gungame.core.sounds.manager import sound_manager
from gungame.core.teams import team_names
from gungame.core.weapons.manager import weapon_order_manager

# Plugin
from .custom_events import GG_Team_Level_Up, GG_Team_Win
from .gg_teamplay import _teamplay_manager


# =============================================================================
# >> CLASSES
# =============================================================================
class _TeamManager(object):
    def __init__(self, team_number):
        super().__init__()
        self.level = 1
        self.multi_kill = 0
        self.team_number = team_number
        self.name = team_names[self.team_number]

    @property
    def index(self):
        for player in player_dictionary.values():
            if player.team == self.team_number:
                return player.index
        return 0

    @property
    def level_multi_kill(self):
        return weapon_order_manager.active[self.level].multi_kill

    @property
    def level_weapon(self):
        return weapon_order_manager.active[self.level].weapon

    def increase_multi_kill(self):
        self.multi_kill += 1
        if self.level_multi_kill < self.multi_kill:
            return
        if self.level == weapon_order_manager.max_levels:
            self.declare_winner()
        else:
            self.increase_level(levels=1)

    def increase_level(self, levels):
        if not isinstance(levels, int) or levels < 1:
            raise ValueError(
                'Invalid value given for levels "{levels}".'.format(
                    levels=levels,
                )
            )
        self.multi_kill = 0
        self.level += levels
        with GG_Team_Level_Up() as event:
            event.team = self.team_number
            event.old_level = self.level - 1
            event.name = self.level
            event.style = _teamplay_manager.current_module

    def declare_winner(self):
        with GG_Team_Win() as event:
            event.winner = self.team_number
            event.loser = 5 - self.team_number
            event.style = _teamplay_manager.current_module

    def send_level_up_message(self, old_level):
        current_level = self.level
        other_level = team_dictionary[5 - self.team_number].level
        if other_level < old_level:
            message = 'Increase'
        elif other_level > current_level:
            message = 'Trailing'
        elif old_level == current_level:
            message = 'Tied'
        else:
            message = 'TakeLead'
        message_manager.chat_message(
            message='TeamPlay:Level:{message}'.format(
                message=message,
            ),
            index=self.index,
            team=self,
            levels=abs(current_level - other_level),
        )

team_dictionary = {
    team_number: _TeamManager(team_number) for team_number in team_names.keys()
}


# =============================================================================
# >> GUNGAME EVENTS
# =============================================================================
@Event('gg_team_level_up')
def _handle_level_up(game_event):
    team_dictionary[game_event['team']].send_level_up_message(
        game_event['old_level']
    )
