# ../gungame/plugins/included/gg_deathmatch/gg_deathmatch.py

"""Plugin that respawns players when the die."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from commands import CommandReturn
from commands.client import ClientCommand
from events import Event
from listeners import OnLevelShutdown
from listeners.tick import Repeat, RepeatStatus
from players.entity import Player
from players.helpers import userid_from_index

# GunGame
from gungame.core.players.dictionary import player_dictionary
from gungame.core.status import GunGameMatchStatus, GunGameStatus

# Plugin
from .configuration import delay


# =============================================================================
# >> CLASSES
# =============================================================================
class DMPlayer(Player):
    """Class used to interact with a specific player."""

    def __init__(self, index):
        """Store the Repeat instance for the player."""
        super().__init__(index)
        self.repeat = Repeat(self._countdown, cancel_on_level_end=True)

    def start_repeat(self):
        """Start the player's respawn countdown."""
        self.repeat.start(1, max(delay.get_int(), 1))

    def _countdown(self):
        """Send messages about impending respawn and respawns the player."""
        # Is the player alive?
        if not self.dead:

            # No need to respawn them
            return

        # Does the player's repeat have more loops remaining?
        if self.repeat.loops_remaining:

            # Message the player with the countdown
            player_dictionary[self.userid].hint_message(
                "DeathMatch:CountDown",
                seconds=self.repeat.loops_remaining,
            )

        # Are there no more loops remaining for the player?
        else:

            # Message the player that they are respawning
            player_dictionary[self.userid].hint_message(
                "DeathMatch:Respawning",
            )

            # Respawn the player
            self.spawn()

    def stop_repeat(self):
        """Stop the player's repeat."""
        self.repeat.stop()

    def is_repeat_active(self):
        """Return whether the player's repeat is running."""
        return self.repeat.status == RepeatStatus.RUNNING


class _DeathMatchPlayers(dict):
    """Dictionary class used to store DMPlayer instances."""

    def __missing__(self, userid):
        """Return a DMPlayer instance for the given userid."""
        value = self[userid] = DMPlayer.from_userid(userid)
        return value

    def __delitem__(self, userid):
        """Stop the player's repeat before removing them."""
        # Is the player in the dictionary?
        if userid not in self:
            return

        # Stop the player's repeat
        self[userid].stop_repeat()

        # Remove the player from the dictionary
        super().__delitem__(userid)

    def clear(self):
        """Loop through all userids to call __delitem__ on them."""
        for userid in list(self):
            del self[userid]


deathmatch_players = _DeathMatchPlayers()


# =============================================================================
# >> REGISTERED CALLBACK
# =============================================================================
@ClientCommand("jointeam")
def _jointeam(command, index):
    """Cancel a player's repeat if they join spectators."""
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return None

    # Is the player joining spectators?
    if command[1] != 1:

        # If not, just return
        return CommandReturn.CONTINUE

    # Get the player's userid
    userid = userid_from_index(index)

    # Get the player's DMPlayer instance
    player = deathmatch_players[userid]

    # Is the player's repeat active?
    if player.is_repeat_active():

        # Message the player about cancelling their respawn
        player_dictionary[userid].hint_message("DeathMatch:CancelTeam")

        # Stop the player's repeat
        player.stop_repeat()

    # Return from the command
    return CommandReturn.CONTINUE


@ClientCommand("joinclass")
def _joinclass(command, index):
    """Hooks joinclass to start a player's repeat."""
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return None

    # Get the player's userid
    userid = userid_from_index(index)

    # Start the player's repeat
    deathmatch_players[userid].start_repeat()

    # Return from the command
    return CommandReturn.CONTINUE


# =============================================================================
# >> EVENTS
# =============================================================================
@Event("player_spawn")
def _player_spawn(game_event):
    """Start bot repeats in case they join mid round."""
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    # Get the player's userid
    userid = game_event["userid"]

    # Get the player's DMPlayer instance
    player = deathmatch_players[userid]

    # Is the player a bot?
    if player.is_fake_client():

        # Start the player's repeat
        player.start_repeat()


@Event("player_death")
def _player_death(game_event):
    """Start the player's repeat when they are killed."""
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    # Get the player's userid
    userid = game_event["userid"]

    # Start the player's repeat
    deathmatch_players[userid].start_repeat()


@Event("player_disconnect")
def _player_disconnect(game_event):
    """Remove the player from the dictionary."""
    del deathmatch_players[game_event["userid"]]


# =============================================================================
# >> LISTENERS
# =============================================================================
@OnLevelShutdown
def _level_shutdown():
    """Clear the deathmatch_players dictionary on map change."""
    deathmatch_players.clear()
