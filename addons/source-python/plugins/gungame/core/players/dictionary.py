# ../gungame/core/players/dictionary.py

"""Player storage dictionary."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import defaultdict

# Source.Python
from players.helpers import userid_from_index

# GunGame
from .attributes import player_attributes
from .instance import GunGamePlayer


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    '_PlayerDictionary',
    'player_dictionary',
)


# =============================================================================
# >> CLASSES
# =============================================================================
class _PlayerDictionary(dict):
    """Dictionary used to store players for GunGame."""

    _removed_players = defaultdict(dict)

    def __missing__(self, userid):
        """Add a player to the dictionary."""
        try:
            # Get the GunGamePlayer instance for the userid
            player = self[userid] = GunGamePlayer.from_userid(userid)
        except OverflowError:
            return None

        # Loop through all items in the dictionary
        for unique_id in self._removed_players:

            # Does the current unique_id equal the given player's unique_id?
            if unique_id == player.uniqueid:

                # Break the loop
                break

        # Was no previous instance found for the player?
        else:

            # Set instance to None
            unique_id = None

        # Loop through all registered attributes
        for attribute in player_attributes:

            # Does the previous instance have the given attribute?
            if (
                unique_id in self._removed_players and
                attribute in self._removed_players[unique_id]
            ):

                # Set the player's attribute to the previous instance's
                setattr(
                    player,
                    attribute,
                    self._removed_players[unique_id][attribute],
                )

            # Does the previous instance not have the given attribute?
            else:

                # Set the player's attribute to the default value
                setattr(
                    player,
                    attribute,
                    player_attributes[attribute],
                )

        # Return the current instance
        return player

    def from_index(self, index):
        """Return the player's instance from their index."""
        return self[userid_from_index(index)]

    def safe_remove(self, userid):
        """Store the player's values in case they rejoin."""
        if userid not in self:
            return
        unique_id = self[userid].uniqueid
        for attribute in player_attributes:
            self._removed_players[unique_id][attribute] = getattr(
                self[userid],
                attribute,
                player_attributes[attribute]
            )
        self[userid].cancel_protect_delay()
        del self[userid]

    def clear(self):
        """Clear the removed players dictionary and the player dictionary."""
        self._removed_players.clear()
        super().clear()


player_dictionary = _PlayerDictionary()
