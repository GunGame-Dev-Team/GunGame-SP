# ../gungame/plugins/included/gg_deathmatch/gg_deathmatch.py

"""Plugin that respawns players when the die."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Commands
from commands import CommandReturn
from commands.client import ClientCommand
#   Events
from events import Event
#   Listeners
from listeners import LevelShutdown
from listeners.tick import TickRepeat
from listeners.tick import TickRepeatStatus
#   Players
from players.entity import PlayerEntity
from players.helpers import index_from_userid
from players.helpers import userid_from_playerinfo

# GunGame Imports
#   Players
from gungame.core.players.dictionary import player_dictionary

# Plugin Imports
from .configuration import delay


# =============================================================================
# >> CLASSES
# =============================================================================
class Player(PlayerEntity):
    """Class used to interact with a specific player."""

    def __init__(self, index):
        """Store the TickRepeat instance for the player."""
        super(Player, self).__init__(index)
        self._repeat = TickRepeat(self._countdown)

    @property
    def repeat(self):
        """Return the player's TickRepeat instance."""
        return self._repeat

    def start_repeat(self):
        """Start the player's respawn countdown."""
        self.repeat.start(1, delay.get_int())

    def _countdown(self):
        """Send messages about impending respawn and respawns the player."""
        # Is the player alive?
        if not self.isdead:

            # No need to respawn them
            return

        # Does the player's repeat have more loops remaining?
        if self.repeat.remaining:

            # Message the player with the countdown
            player_dictionary[self.userid].hint_message(
                'DeathMatch_Respawn_CountDown', seconds=self.repeat.remaining)

        # Are there no more loops remaining for the player?
        else:

            # Message the player that they are respawning
            player_dictionary[self.userid].hint_message(
                'DeathMatch_Respawning')

            # Respawn the player
            self.respawn()

    def stop_repeat(self):
        """Stop the player's repeat."""
        self.repeat.stop()

    def is_repeat_active(self):
        """Return whether the player's repeat is running."""
        return self.repeat.status == TickRepeatStatus.RUNNING


class _DeathMatchPlayers(dict):
    """Dictionary class used to store Player instances."""

    def __missing__(self, userid):
        """Return a Player instance for the given userid."""
        # Store the userid's value as a Player instance
        value = self[userid] = Player(index_from_userid(userid))

        # Return the Player instance
        return value

    def __delitem__(self, userid):
        """Stop the player's repeat before removing them."""
        # Is the player in the dictionary?
        if userid in self:

            # Stop the player's repeat
            self[userid].stop_repeat()

        # Remove the player from the dictionary
        super(_DeathMatchPlayers, self).__delitem__(userid)

    def clear(self):
        """Loop through all userids to call __delitem__ on them."""
        for userid in list(self):
            del self[userid]

# Get the _DeathMatchPlayers instance
deathmatch_players = _DeathMatchPlayers()


# =============================================================================
# >> REGISTERED CALLBACK
# =============================================================================
@ClientCommand('jointeam')
def jointeam(playerinfo, command):
    """Cancel a player's repeat if they join spectators."""
    # Is the player joining spectators?
    if command[1] != 1:

        # If not, just return
        return CommandReturn.CONTINUE

    # Get the player's userid
    userid = userid_from_playerinfo(playerinfo)

    # Get the player's Player instance
    player = deathmatch_players[userid]

    # Is the player's repeat active?
    if player.is_repeat_active():

        # Message the player about cancelling their respawn
        player_dictionary[userid].hint_message('DeathMatch_CancelTeam')

        # Stop the player's repeat
        player.stop_repeat()

    # Return from the command
    return CommandReturn.CONTINUE


@ClientCommand('joinclass')
def joinclass(playerinfo, command):
    """Hook joinclass to start a player's repeat."""
    # Get the player's userid
    userid = userid_from_playerinfo(playerinfo)

    # Start the player's repeat
    deathmatch_players[userid].start_repeat()

    # Return from the command
    return CommandReturn.CONTINUE


# =============================================================================
# >> EVENTS
# =============================================================================
@Event('player_spawn')
def player_spawn(game_event):
    """Start bot repeats in case they join mid round."""
    # Get the player's userid
    userid = game_event['userid']

    # Get the player's Player instance
    player = deathmatch_players[userid]

    # Is the player a bot?
    if player.is_fake_client():

        # Start the player's repeat
        player.start_repeat()


@Event('player_death')
def player_death(game_event):
    """Start the player's repeat when they are killed."""
    # Get the player's userid
    userid = game_event['userid']

    # Start the player's repeat
    deathmatch_players[userid].start_repeat()


@Event('player_disconnect')
def player_disconnect(game_event):
    """Remove the player from the dictionary."""
    del deathmatch_players[game_event['userid']]


# =============================================================================
# >> LISTENERS
# =============================================================================
@LevelShutdown
def level_shutdown():
    """Clear the deathmatch_players dictionary on map change."""
    deathmatch_players.clear()
