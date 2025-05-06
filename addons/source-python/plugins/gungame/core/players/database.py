# ../gungame/core/players/database.py

"""Stores winner information for all players."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import defaultdict
from contextlib import suppress
from itertools import chain
from sqlite3 import DatabaseError, connect
from time import time

# GunGame
from ..config.misc import prune_database
from ..paths import GUNGAME_DATA_PATH

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "winners_database",
)


# =============================================================================
# >> CLASSES
# =============================================================================
# ruff: noqa: UP031, S608
class _PlayerDatabase:
    """Class used to hold values for a player in the winner database."""

    def __init__(self):
        """Store the base values on creation."""
        self.name = None
        self.time_stamp = time()
        self.last_win = None
        self.wins = 0


class _WinsDatabase(defaultdict):
    """Database to store player wins."""

    def __init__(self, default_factory):
        """Create the dictionary and gather any stored values."""
        super().__init__(default_factory)

        # Establish the SQL connection
        self.connection = connect(GUNGAME_DATA_PATH / "winners.db")
        self.connection.text_factory = str

        # Get the cursor
        self.cursor = self.connection.cursor()

        # Create the gungame_winners table if it does not already exist
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS gungame_winners(
              unique_id VARCHAR(20),
              name VARCHAR(31),
              wins VARCHAR(10) DEFAULT 0,
              time_stamp VARCHAR(31),
              last_win VARCHAR(31),
              PRIMARY KEY(unique_id DESC)
            )
            """,
        )
        self.cursor.execute("PRAGMA auto_vacuum = 1")

    def load_database(self):
        """Fill the dictionary with the data from the stored database."""
        # If there is already data, do not load
        if self:
            msg = "Data already loaded!"
            raise DatabaseError(msg)

        # Gather all data from the table
        data = self.cursor.execute(
            """
            SELECT unique_id, name, wins, time_stamp, last_win
              FROM gungame_winners
            """,
        )
        data = data.fetchall()

        # Are there no winners to add?
        if not data:
            return

        # Loop through all the past winners and their data
        for unique_id, name, wins, time_stamp, last_win in data:

            # Add the current winner to the database
            instance = self[unique_id]
            instance.name = name
            instance.wins = int(wins)
            instance.time_stamp = float(time_stamp)
            instance.last_win = float(last_win)

    def set_player_wins(self, player, wins):
        """Update the player's database values."""
        # Get the current time stamp
        time_stamp = time()

        # Is this a new winner?
        if player.uniqueid not in self:

            # Add the new winner to the database
            self.cursor.execute(
                """
                INSERT INTO gungame_winners (
                  name, unique_id, wins, time_stamp, last_win
                ) VALUES(?, ?, ?, ?, ?)
                """,
                (player.name, player.uniqueid, 0, time_stamp, time_stamp),
            )

        # Get the winner's instance
        instance = self[player.uniqueid]

        # Set the values for the instance
        instance.name = player.name
        instance.wins = wins
        instance.time_stamp = time_stamp
        instance.last_win = time_stamp

        # Update the winner's values in the database
        self.cursor.execute(
            """
            UPDATE gungame_winners
              SET name=?, time_stamp=?, wins=?, last_win=?
              WHERE unique_id=?
             """,
            (
                player.name,
                instance.time_stamp,
                instance.wins,
                instance.last_win,
                player.uniqueid,
            ),
        )

        # Commit the changes to the database
        self.connection.commit()

    def update_player_time_stamp(self, player):
        """
        Update the player's time stamp.

        This occurs on player_activate and is stored for pruning purposes.
        """
        # Is the player not in the database?
        if player.uniqueid not in self:
            msg = "Player not in database."
            raise KeyError(msg)

        # Get the player's instance
        instance = self[player.uniqueid]

        # Store the player's current name
        instance.name = player.name

        # Store the player's new time stamp
        instance.time_stamp = time()

        # Update the player's name and time stamp in the database
        self.cursor.execute(
            """
            UPDATE gungame_winners
              SET name=?, time_stamp=?
              WHERE unique_id=?
            """,
            (player.name, instance.time_stamp, player.uniqueid),
        )

        # Commit the changes to the database
        self.connection.commit()

    def prune_database(self):
        """Remove players from the database who haven't played in a while."""
        # 0 = do not prune
        days = abs(prune_database.get_int())
        if not days:
            return

        # Retrieve all the unique ids to prune from the database
        self.cursor.execute(
            """
            SELECT unique_id
              FROM gungame_winners
              WHERE time_stamp < strftime("%s", "now", "-%s days")
            """ % ("%s", days),
        )
        unique_ids = list(chain.from_iterable(self.cursor.fetchall()))

        # Are there any to prune?
        if not unique_ids:
            return

        # Remove the users from the database
        self.cursor.execute(
            """
            DELETE FROM gungame_winners
              WHERE unique_id IN ("%s")
            """ % ('","'.join(unique_ids)),
        )
        self.connection.commit()

        # Remove the users from the dictionary
        for unique_id in unique_ids:
            with suppress(KeyError):
                del self[unique_id]


winners_database = _WinsDatabase(_PlayerDatabase)
