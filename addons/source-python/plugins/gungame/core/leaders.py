# ../gungame/core/leaders.py

"""Tracks the leader and calls leader based events."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from contextlib import suppress

# Source.Python
from filters.players import PlayerIter
from players.helpers import index_from_userid

# GunGame
from .events.included.leaders import (
    GG_Leader_Disconnect, GG_Leader_Lost_Level, GG_New_Leader, GG_Tied_Leader,
)
from .messages.manager import message_manager
from .players.dictionary import player_dictionary


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    '_LeaderManager',
    'leader_manager',
)


# =============================================================================
# >> CLASSES
# =============================================================================
class _LeaderManager(dict):
    """Class used to track leaders."""

    def __init__(self):
        """Add all current players to the dictionary."""
        # Initialize the dictionary
        super().__init__()

        # Loop through all current players
        for userid in [player.userid for player in PlayerIter()]:

            # Add the player to the level dictionary
            self[userid] = player_dictionary[userid].level

    def __delitem__(self, userid):
        """Validate that the userid is in the dictionary before deletion."""
        if userid in self:
            super().__delitem__(userid)

    @property
    def leader_level(self):
        """Return the level of the leader."""
        return max(
            list(
                filter(
                    None,
                    self.values()
                )
            ) or [1]
        )

    @property
    def current_leaders(self):
        """Return a list of current leaders."""
        # Get the current leader level
        level = self.leader_level

        # Are there no leaders?
        if level == 1:
            return None

        # Return a list of players on the leader level
        leaders = []
        for userid in self:
            if self[userid] == level:
                with suppress(ValueError):
                    index_from_userid(userid)
                    leaders.append(userid)
        return leaders

    def is_leading(self, userid):
        """Return whether the given player is a leader or not."""
        return self.get(userid) == self.leader_level != 1

    def add_player(self, userid):
        """Add the player to the dictionary."""
        self[userid] = player_dictionary[userid].level

    def player_level_up(self, userid):
        """Set the player's level and see if the leaders changed."""
        # Get the player's new level
        player_level = player_dictionary[userid].level
        if player_level < self.leader_level:
            return
        old_leaders = self._get_leader_string()
        old_level = self.leader_level
        player = player_dictionary[userid]
        self[userid] = player.level
        new_leaders = self._get_leader_string()
        new_level = self.leader_level
        count = len(self.current_leaders)
        if count > 1:
            with GG_Tied_Leader() as event:
                event.userid = event.leveler = userid
                event.old_leaders = old_leaders
                event.leaders = new_leaders
                event.leader_level = new_level
            tied_type = 'Singular' if count == 2 else 'Plural'
            message = f'Leader:Tied:{tied_type}'
            message_manager.chat_message(
                message,
                player.index,
                count=count,
                player=player,
            )
        else:
            with GG_New_Leader() as event:
                event.userid = event.leveler = userid
                event.old_leaders = old_leaders
                event.old_level = old_level
                event.leaders = new_leaders
                event.leader_level = new_level
            message_manager.chat_message(
                'Leader:New:Singular',
                player.index,
                player=player,
            )

    def player_level_down(self, userid):
        """Set the player's level and see if the leaders changed."""
        if not self.is_leading(userid):
            self[userid] = player_dictionary[userid].level
            return
        old_leaders = self._get_leader_string()
        old_level = self[userid]
        self[userid] = player_dictionary[userid].level
        new_level = self.leader_level
        with GG_Leader_Lost_Level() as event:
            event.userid = event.leveler = userid
            event.old_leaders = old_leaders
            event.old_level = old_level
            event.leaders = self._get_leader_string()
            event.leader_level = new_level
        self._check_new_leaders(userid)

    def check_disconnect(self, userid):
        """Remove the player and see if the leaders changed."""
        if not self.is_leading(userid):
            del self[userid]
            return
        old_leaders = self._get_leader_string()
        old_level = self[userid]
        del self[userid]
        with GG_Leader_Disconnect() as event:
            event.userid = userid
            event.old_leaders = old_leaders
            event.old_level = old_level
            event.leaders = self._get_leader_string()
            event.leader_level = self.leader_level
        self._check_new_leaders(userid)

    def _check_new_leaders(self, userid):
        """Check to see if the leaders changed and send messages."""
        current = self.current_leaders
        if current is None or (len(current) == 1 and userid in current):
            return
        level = self.leader_level
        if len(current) == 1:
            try:
                player = player_dictionary[current[0]]
            except ValueError:
                return
            message_manager.chat_message(
                'Leader:New:Singular',
                player.index,
                player=player,
            )
        else:
            names = [player_dictionary[player].name for player in current]
            message_manager.chat_message(
                'Leader:New:Plural',
                names=names,
                level=level,
            )

    def _get_leader_string(self):
        """Return a string of leader userids."""
        leaders = self.current_leaders
        if leaders is None:
            return ''
        return ','.join(map(str, leaders))


leader_manager = _LeaderManager()
