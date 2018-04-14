# ../gungame/plugins/included/gg_teamwork/gg_teamwork.py

"""Plugin that levels players up individually to win as a team."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from contextlib import suppress

# Source.Python
from colors import BLUE, RED, WHITE
from cvars import ConVar
from engines.server import queue_command_string
from entities.entity import Entity
from events import Event
from events.hooks import EventAction, PreEvent
from listeners import OnLevelInit
from listeners.tick import Delay
from players.teams import teams_by_number

# Site-package
from mutagen import MutagenError

# GunGame
from gungame.core.config.misc import dynamic_chat_time
from gungame.core.messages.hooks import MessagePrefixHook
from gungame.core.messages.manager import message_manager
from gungame.core.players.dictionary import player_dictionary
from gungame.core.sounds.manager import sound_manager
from gungame.core.status import GunGameMatchStatus, GunGameStatus
from gungame.core.teams import team_levels, team_names
from gungame.core.weapons.manager import weapon_order_manager

# Plugin
from .configuration import join_team_level
from .custom_events import GG_Team_Win


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def unload():
    """Clear the team level dictionary."""
    team_levels.clear()


# =============================================================================
# >> CLASSES
# =============================================================================
class _TeamManager(dict):
    """Dictionary class to store teams with their info."""

    def __init__(self):
        super().__init__()
        for number in team_levels:
            self[number] = _TeamManagement(number)

    def clear(self):
        team_levels.clear()
        for team in self.values():
            team.reset_values()

    def set_player_levels(self):
        for team in self.values():
            team.set_team_player_levels()


class _TeamManagement(object):
    """Class used to interact with a specific team and its information."""

    def __init__(self, number):
        """Store all of the team information."""
        self.number = number
        self.alias = teams_by_number[self.number]
        self.level = 1
        self._name = team_names[self.number]
        self._leader = None
        self.leader_userid = None

    @property
    def name(self):
        """Return the team's name."""
        if self._name is None:
            self._name = team_names.get(self.number)
        return self._name

    @property
    def index(self):
        """Return the index of the team's leader."""
        return self.leader.index if self.leader is not None else 0

    @property
    def leader(self):
        """Return the team's current leader."""
        return self._leader

    @leader.setter
    def leader(self, player):
        """Set the team's leader."""
        current = self._leader
        self._leader = player
        self.leader_userid = None if player is None else player.userid
        if current is None or player is None:
            team_levels[self.number] = 1
            return
        team_levels[self.number] = player.level
        if (
            (
                current.level < player.level or
                current.userid == player.userid
            ) and player.level < weapon_order_manager.max_levels
        ):
            message_manager.chat_message(
                message='TeamWork:Leader:Increase',
                index=self.index,
                player=player.name,
                team_name=self.name,
                level=self.leader_level,
            )

    @property
    def leader_level(self):
        """Return the team leader's level."""
        return None if self.leader is None else self.leader.level

    @property
    def color(self):
        """Return the team's color."""
        return RED if self.number == 2 else BLUE

    def set_team_player_levels(self):
        """Set the level for all players on the team."""
        if self.leader_level is None:
            self.find_team_leader()
        self.level = self.leader_level
        if self.level is None:
            return
        for player in player_dictionary.values():
            if player.team_index != self.number:
                continue
            if player.level == self.level:
                continue
            player.level = self.level
            player.multi_kill = 0

    def set_joining_player_level(self, player):
        """Set the level of the player who joined the team."""
        level = self.level if join_team_level.get_int() else 1
        if level is None:
            level = self.level = 1
        player.level = level

    def find_team_leader(self, leveler=None, old_level=None, disconnect=False):
        """Find the team's current leader."""
        team_players = {
            player.level: player for player in player_dictionary.values()
            if player.team_index == self.number and player.level is not None
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
        """Send a message about the team's level."""
        if self.leader_level is None:
            return
        message_manager.chat_message(
            message='TeamWork:TeamLevel',
            index=self.index,
            team_name=self.name,
            level=self.leader_level,
            weapon=weapon_order_manager.active[self.leader_level].weapon,
        )

    def reset_values(self):
        """Reset the team's values."""
        self._leader = None
        self.level = 1

teamwork_manager = _TeamManager()


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_team')
def _check_team_leaders(game_event):
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    userid = game_event['userid']
    old_team_number = game_event['oldteam']

    old_team = teamwork_manager.get(old_team_number)
    if old_team and old_team.leader_userid == userid:
        old_team.find_team_leader(disconnect=True)

    new_team = teamwork_manager.get(game_event['team'])
    if not new_team:
        return

    if not old_team_number:
        new_team.set_joining_player_level(player_dictionary[userid])

    else:
        new_team.find_team_leader()


@Event('round_start')
def _send_level_messages(game_event):
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    for team in teamwork_manager.values():
        team.send_level_message()


@Event('round_end')
def _sync_player_levels(game_event):
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    Delay(
        delay=0,
        callback=teamwork_manager.set_player_levels,
    )


# =============================================================================
# >> GUNGAME EVENTS
# =============================================================================
@Event('gg_start')
@OnLevelInit
def _clear_team_dictionary(game_event=None):
    teamwork_manager.clear()


@Event('gg_level_up')
def _level_up(game_event):
    player = player_dictionary[game_event['leveler']]
    team = teamwork_manager[player.team_index]
    if (
        team.leader_userid in (None, player.userid) or
        team.leader_level < game_event['new_level']
    ):
        team.leader = player


@Event('gg_level_down')
def _check_team_decrease(game_event):
    player = player_dictionary[game_event['leveler']]
    team = teamwork_manager[player.team_index]
    if team.leader.userid == player.userid:
        team.find_team_leader(player, game_event['old_level'])


@Event('gg_team_win')
def _end_match(game_event):
    # Set the match status
    GunGameStatus.MATCH = GunGameMatchStatus.POST

    # Get the winning team information
    winning_team = teamwork_manager[game_event['winner']]

    # Send the winner messages
    message_manager.chat_message(
        index=winning_team.index,
        message='TeamWork:Winner:Long',
        team_name=winning_team.name,
    )
    for second in range(4):
        Delay(
            delay=second,
            callback=message_manager.center_message,
            kwargs={
                'message': 'TeamWork:Winner:Short',
                'team_name': winning_team.name,
            },
            cancel_on_level_end=True,
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
    if dynamic_chat_time.get_bool() and winner_sound is not None:
        with suppress(MutagenError):
            ConVar('mp_chattime').set_float(winner_sound.duration)

    # End the match to move to the next map
    entity = Entity.find_or_create('game_end')
    entity.end_game()

    # Do not remove! This fixes a lot of console spam and hanging on map end.
    queue_command_string('bot_kick')

    # Reset the teams
    _clear_team_dictionary()


# =============================================================================
# >> EVENT HOOKS
# =============================================================================
@PreEvent('gg_win')
def _pre_gg_win(game_event):
    team_number = player_dictionary[game_event['winner']].team_index
    Delay(
        delay=0,
        callback=_fire_win_event,
        args=(team_number,),
    )
    return EventAction.BLOCK


# =============================================================================
# >> MESSAGE HOOKS
# =============================================================================
@MessagePrefixHook('Leader:')
def _level_info_hook(message_name, message_prefix):
    """Hook the LevelInfo messages so that the team messages can be sent."""
    return False


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _fire_win_event(team_number):
    with GG_Team_Win() as event:
        event.winner = team_number
        event.loser = 5 - team_number
