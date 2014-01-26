# ../gungame/core/players/dictionary.py

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame Imports
#   Players
from gungame.core.players.attributes import PlayerAttributes
from gungame.core.players.instance import _GunGamePlayer


# =============================================================================
# >> CLASSES
# =============================================================================
class _PlayerDictionary(dict):
    '''Dictionary used to store players for GunGame'''

    def __missing__(self, userid):
        '''Called when a userid is not in the dictionary'''

        # Get the _GunGamePlayer instance for the userid
        player = self[userid] = _GunGamePlayer(userid)

        # Loop through all items in the dictionary
        for other in self:

            # Is this the given player?
            if player == other:

                # If so, continue to the next player
                continue

            # Does the current uniqueid equal the given player's uniqueid?
            if self[other].uniqueid == player.uniqueid:

                # Store the instance
                instance = other

                # Break the loop
                break

        # Was no previous instance found for the player?
        else:

            # Set instance to None
            instance = None

        # Loop through all registered attributes
        for attribute in PlayerAttributes:

            # Does the previous instance have the given attribute?
            if not instance is None and hasattr(self[instance], attribute):

                # Set the player's attribute to the previous instance's
                setattr(player, attribute, getattr(instance, attribute))

            # Does the previous instance not have the given attribute?
            else:

                # Set the player's attribute to the default value
                setattr(player, attribute, PlayerAttributes[attribute].default)

        # Was a previous instance found?
        if not instance is None:

            # Remove the previous instance from the dictionary
            del self[instance]

        # Return the current instance
        return player

# Get the _PlayerDictionary instance
PlayerDictionary = _PlayerDictionary()
