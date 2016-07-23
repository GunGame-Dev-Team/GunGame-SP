# ../gungame/core/players/dictionary.py

"""Player storage dictionary."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from collections import defaultdict

# GunGame Imports
#   Players
from .attributes import player_attributes
from .instance import GunGamePlayer


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('player_dictionary',
           )


# =============================================================================
# >> CLASSES
# =============================================================================
class _PlayerDictionary(dict):
    """Dictionary used to store players for GunGame."""

    _removed_players = defaultdict(dict)

    def __missing__(self, userid):
        """Called when a userid is not in the dictionary."""
        # Get the GunGamePlayer instance for the userid
        player = self[userid] = GunGamePlayer.from_userid(userid)

        # Loop through all items in the dictionary
        for uniqueid in self._removed_players:

            # Does the current uniqueid equal the given player's uniqueid?
            if uniqueid == player.uniqueid:

                # Break the loop
                break

        # Was no previous instance found for the player?
        else:

            # Set instance to None
            uniqueid = None

        # Loop through all registered attributes
        for attribute in player_attributes:

            # Does the previous instance have the given attribute?
            if (uniqueid is not None and
                    attribute in self._removed_players[uniqueid]):

                # Set the player's attribute to the previous instance's
                setattr(
                    player, attribute,
                    self._removed_players[uniqueid][attribute])

            # Does the previous instance not have the given attribute?
            else:

                # Set the player's attribute to the default value
                setattr(
                    player, attribute, player_attributes[attribute].default)

        # Return the current instance
        return player

    def safe_remove(self, userid):
        """Store the player's values in case they rejoin."""
        if userid not in self:
            return
        uniqueid = self[userid].uniqueid
        for attribute in player_attributes:
            self._removed_players[uniqueid][attribute] = getattr(
                self[userid], attribute)
        del self[userid]

    def clear(self):
        """Clear the removed players dictionary and the player dictionary."""
        self._removed_players.clear()
        super().clear()

# Get the _PlayerDictionary instance
player_dictionary = _PlayerDictionary()
