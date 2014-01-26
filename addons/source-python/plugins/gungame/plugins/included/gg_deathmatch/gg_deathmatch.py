# ../gungame/addons/included/gg_deathmatch/gg_deathmatch.py

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
from command_c import CommandReturn
#   Commands
from commands.client import ClientCommand
#   Events
from events import Event
#   Messages
from messages import HintText
#   Players
from players.entity import PlayerEntity
from players.helpers import index_from_userid
from players.helpers import userid_from_playerinfo
#   Tick
from tick.repeat import Repeat
from tick.repeat import Status
#   Translations
from translations.strings import LangStrings


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Get the message strings
deathmatch_strings = LangStrings('gg_deathmatch')

# Store an empty dictionary
Messages = {}

# Loop through each of the message strings
for key in deathmatch_strings:

    # Add the message string to the dictionary as a HintText instance
    Messages[key] = HintText(deathmatch_strings[key])


# =============================================================================
# >> CLASSES
# =============================================================================
class Player(object):
    '''Class used to interact with a specific player'''

    def __init__(self, userid):
        '''Stores the PlayerEntity instace and
            the Repeat instance for the player'''

        # Get the index of the given userid
        index = index_from_userid(userid)

        # Store the PlayerEntity and Repeat instances
        self.player = PlayerEntity(index)
        self._repeat = Repeat(self._countdown)

    def __getattr__(self, attr):
        '''Override __getattr__ to return attributes from PlayerEntity'''

        # Does PlayerEntity have the given attribute?
        if hasattr(self.player, attr):

            # Get the PlayerEntity's attribute
            return getattr(self.player, attr)

        # Call __getattr__
        return super(Player, self).__getattr__(attr)

    def start_repeat(self):
        '''Starts the player's respawn countdown'''
        self._repeat.start(1, respawn_delay.get_int())

    def _countdown(self):
        '''Sends messages about impending respawn and respawns the player'''

        # Is the player alive?
        if not self.isdead:

            # No need to respawn them
            return

        # Does the player's repeat have more loops remaining?
        if self._repeat.remaining:

            # Message the player with the countdown
            Messages['Respawn CountDown'].tokens = {
                'seconds': self._repeat.remaining}
            Messages['Respawn CountDown'].send(self.index)

        # Are there no more loops remaining for the player?
        else:

            # Message the player that they are respawning
            Messages['Respawning'].send(self.index)

            # Respawn the player
            self.get_prop('m_iPlayerState').set_int(0)
            self.get_prop('m_lifeState').set_int(512)
            self.dispatch_spawn()

    def stop_repeat(self):
        '''Stops the player's repeat'''
        self._repeat.stop()

    def is_repeat_active(self):
        '''Returns whether the player's repeat is running'''
        return self._repeat.status == Status.RUNNING


class _Players(dict):
    '''Dictionary class used to store Player instances'''

    def __missing__(self, userid):
        '''Returns a Player instance for the given userid'''

        # Store the userid's value as a Player instance
        value = self[userid] = Player(userid)

        # Return the Player instance
        return value

# Get the _Players instance
Players = _Players()


# =============================================================================
# >> REGISTERED CALLBACK
# =============================================================================
@ClientCommand('jointeam')
def jointeam(playerinfo, ccommand):
    '''
        jointeam hook used to cancel a player's repeat if they join spectators
    '''

    # Is the player joining spectators?
    if ccommand[1] != 1:

        # If not, just return
        return CommandReturn.CONTINUE

    # Get the player's userid
    userid = userid_from_playerinfo(playerinfo)

    # Get the player's Player instance
    player = Players[userid]

    # Is the player's repeat active?
    if player.is_repeat_active():

        # Message the player about cancelling their respawn
        Messages['Cancel Team'].send(player.index)

        # Stop the player's repeat
        player.stop_repeat()

    # Return from the command
    return CommandReturn.CONTINUE


@ClientCommand('joinclass')
def joinclass(playerinfo, ccommand):
    '''joinclass hook used to start a player's repeat'''

    # Get the player's userid
    userid = userid_from_playerinfo(playerinfo)

    # Start the player's repeat
    Players[userid].start_repeat()

    # Return from the command
    return CommandReturn.CONTINUE


# =============================================================================
# >> EVENTS
# =============================================================================
@Event
def server_spawn(game_event):
    '''Clears the Players dictionary on map change'''
    Players.clear()


@Event
def player_spawn(game_event):
    '''Starts bot repeats in case they join mid round'''

    # Get the player's userid
    userid = game_event.get_int('userid')

    # Get the player's Player instance
    player = Players[userid]

    # Is the player a bot?
    if player.is_fake_client():

        # Start the player's repeat
        player.start_repeat()


@Event
def player_death(game_event):
    '''Starts a player's repeat when they are killed'''

    # Get the player's userid
    userid = game_event.get_int('userid')

    # Start the player's repeat
    Players[userid].start_repeat()
