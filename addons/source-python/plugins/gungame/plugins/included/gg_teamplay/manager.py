# ../gungame/plugins/included/gg_teamplay/manager.py

"""Teamplay management."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from colors import BLUE, RED, WHITE
from cvars import ConVar
from entities.entity import Entity
from events import Event
from listeners.tick import Delay

# GunGame
from gungame.core.config.misc import dynamic_chat_time
from gungame.core.messages import message_manager
from gungame.core.players.dictionary import player_dictionary
from gungame.core.sounds.manager import sound_manager
from gungame.core.status import GunGameMatchStatus, GunGameStatus
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

    @property
    def name(self):
        return team_names[self.team_number]

    @property
    def index(self):
        for player in player_dictionary.values():
            if player.team == self.team_number:
                return player.index
        return 0

    @property
    def level_multi_kill(self):
        return (
            weapon_order_manager.active[self.level].multi_kill *
            self._get_multi_kill_multiplier()
        )

    @property
    def level_weapon(self):
        return weapon_order_manager.active[self.level].weapon

    def _get_multi_kill_multiplier(self):
        if _teamplay_manager.current_module != 'deathmatch':
            return 1

        # TODO: add melee/nade conditionals

        return len(
            [x for x in player_dictionary if x.team == self.team_number]
        )

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

    def send_multi_kill_message(self):
        current_level = self.level
        other_team = team_dictionary[5 - self.team_number]
        message = 'TeamPlay:MultiKill:'
        if current_level > other_team.level:
            message += 'Leading'
        elif current_level < other_team.level:
            message += 'Trailing'
        else:
            message += 'Tied'
        message_manager.chat_message(
            message=message,
            index=self.index,
            team=self,
            other=other_team,
            levels=abs(current_level - other_team.level)
        )

    def send_level_up_message(self, old_level):
        current_level = self.level
        other_level = team_dictionary[5 - self.team_number].level
        message = 'TeamPlay:Level:'
        if other_level < old_level:
            message += 'Increase'
        elif other_level > current_level:
            message += 'Trailing'
        elif old_level == current_level:
            message += 'Tied'
        else:
            message += 'TakeLead'
        message_manager.chat_message(
            message=message,
            index=self.index,
            team=self,
            levels=abs(current_level - other_level),
        )

    def send_current_level_message(self):
        message = 'TeamPlay:Round'
        if self.multi_kill:
            message += ':MultiKill'
        message_manager.chat_message(
            message=message,
            team=self,
        )

team_dictionary = {
    team_number: _TeamManager(team_number) for team_number in team_names.keys()
}


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_spawn')
def _send_level_info(game_event):
    pass


# =============================================================================
# >> GUNGAME EVENTS
# =============================================================================
@Event('gg_team_level_up')
def _handle_level_up(game_event):
    team_dictionary[game_event['team']].send_level_up_message(
        game_event['old_level']
    )


@Event('gg_team_win')
def _handle_team_win(game_event):
    # Set the match status
    GunGameStatus.MATCH = GunGameMatchStatus.POST

    # Get the winning team information
    winning_team = team_dictionary[game_event['winner']]

    # Send the winner messages
    message_manager.chat_message(
        index=winning_team.index,
        message='TeamPlay:Winner:Long',
        team=winning_team,
    )
    for second in range(4):
        Delay(
            second,
            message_manager.center_message,
            kwargs={
                'message': 'TeamPlay:Winner:Short',
                'team': winning_team,
            }
        )
    color = {2: RED, 3: BLUE}.get(winning_team.team_number, WHITE)
    message_manager.top_message(
        message='TeamPlay:Winner:Short',
        color=color,
        team=winning_team,
    )

    # Play the winner sound
    winner_sound = sound_manager.play_sound('winner')

    # Set the dynamic chat time, if needed
    if dynamic_chat_time.get_bool():
        ConVar('mp_chattime').set_float(winner_sound.duration)

    # End the match to move to the next map
    entity = Entity.find_or_create('game_end')
    entity.end_game()
