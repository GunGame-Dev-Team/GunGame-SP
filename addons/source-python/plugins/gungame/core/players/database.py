# ../gungame/core/players/database.py

"""Stores winner information for all players."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Collections
from collections import defaultdict
#   SQLite3
from sqlite3 import connect
#   Time
from time import time

# GunGame Imports
#   Paths
from gungame.core.paths import GUNGAME_DATA_PATH


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('winners_database',
           )


# =============================================================================
# >> CLASSES
# =============================================================================
class _PlayerDatabase(object):
    """Class used to hold values for a player in the winners database."""

    def __init__(self):
        """Store the base values on creation."""
        self.time_stamp = time()
        self.last_win = None
        self.wins = 0


class _WinsDatabase(defaultdict):
    """Database to store player wins."""

    def __init__(self, default_factory):
        """Create the dictionary and gather any stored values."""
        # Create the defaultdict instance
        super().__init__(default_factory)

        # Establish the SQL connection
        self._connection = connect(GUNGAME_DATA_PATH / 'winners.db')
        self.connection.text_factory = str

        # Get the cursor
        self._cursor = self.connection.cursor()

        # Create the gungame_winners table if it does not already exist
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS gungame_winners(uniqueid varchar(20), '
            'name varchar(31), wins varchar(10) DEFAULT 0, time_stamp '
            'varchar(31), last_win varchar(31), PRIMARY KEY(uniqueid DESC))')
        self.cursor.execute('PRAGMA auto_vacuum = 1')

        # Gather all data from the table
        data = self.cursor.execute(
            'SELECT uniqueid, wins, time_stamp, last_win FROM gungame_winners')
        data = data.fetchall()

        # Are there no winners to add?
        if not data:
            return

        # Loop through all the past winners and their data
        for uniqueid, wins, time_stamp, last_win in data:

            # Add the current winner to the database
            instance = self[uniqueid]
            instance.wins = int(wins)
            instance.time_stamp = float(time_stamp)
            instance.last_win = float(last_win)

    @property
    def connection(self):
        """Return the SQL connection."""
        return self._connection

    @property
    def cursor(self):
        """Return the SQL cursor."""
        return self._cursor

    def increment_player_wins(self, player):
        """Update the player's database values."""
        # Is this a new winner?
        if player.uniqueid not in self:

            # Add the new winner to the database
            self.cursor.execute(
                'INSERT INTO gungame_winners (name, uniqueid, wins, '
                'time_stamp, last_win) VALUES(?, ?, ?, ?, ?)',
                (player.name, player.uniqueid, 0, time_stamp, time_stamp))

        # Get the current time stamp
        time_stamp = time()

        # Get the winner's instance
        instance = self[player.uniqueid]

        # Set the values for the instance
        instance.wins += 1
        instance.time_stamp = time_stamp
        instance.last_win = time_stamp

        # Update the winner's values in the database
        self.cursor.execute(
            'UPDATE gungame_winners SET name=?, time_stamp=?, '
            'wins=?, last_win=? WHERE uniqueid=?',
            (player.name, instance.time_stamp, instance.wins,
            instance.last_win, player.uniqueid))

        # Commit the changes to the database
        self.connection.commit()

    def update_player_time_stamp(self, player):
        """Update the player's time stamp.

        This occurs on player_activate and is stored for pruning purposes.
        """
        # Is the player not in the database?
        if player.uniqueid not in self:
            raise KeyError('Player not in database.')

        # Get the player's instance
        instance = self[player.uniqueid]

        # Store the player's new time stamp
        instance.time_stamp = time()

        # Update the player's name and time stamp in the database
        self.cursor.execute(
            'UPDATE gungame_winners SET name=?, time_stamp=? WHERE uniqueid=?',
            (player.name, instance.time_stamp, player.uniqueid))

        # Commit the changes to the database
        self.connection.commit()

# The singleton object for the _WinsDatabase class.
winners_database = _WinsDatabase(_PlayerDatabase)
