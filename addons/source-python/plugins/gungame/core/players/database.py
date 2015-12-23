# ../gungame/core/players/database.py

"""Stores winner information for all players."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   SQLite3
from sqlite3 import connect

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
class _WinsDatabase(object):
    """Database to store player wins."""

    def __init__(self):
        self.connection = connect(GUNGAME_DATA_PATH / 'winners.db')
        self.connection.text_factory = str
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS WINNERS (name varchar(31), """
            """uniqueid TEXT UNIQUE, wins INT DEFAULT 0, """
            """timestamp varchar(31), PRIMARY KEY (uniqueid DESC))""")
        self.cursor.execute('PRAGMA auto_vacuum FULL')
        self.commit()

    def commit(self):
        """Commit the changes."""
        if self.connection.total_changes:
            self.connection.commit()

    def update_timestamp(self, player):
        """Update the player's timestamp."""
        self.cursor.execute(
            """UPDATE WINNERS SET name=?, timestamp=? WHERE uniqueid=?""",
            (player.name, 'strftime("%s", "now")', player.uniqueid))

# The singleton object for the _WinsDatabase class.
winners_database = _WinsDatabase()


class _PlayerDatabase(object):
    """Player wins/ranks functionality."""

    def _get_wins(self):
        """Return the number of wins the player has."""
        return int(winners_database.select(
            'WINNERS', 'wins', 'where uniqueid = "{0}"'.format(
                self.uniqueid)) or 0)

    def _set_wins(self, value):
        """Set the number of wins for the player."""
        if self.is_fake_client():
            return
        if self.wins:
            pass
        else:
            pass

    wins = property(_get_wins, _set_wins, '')

    def update_timestamp(self):
        """Update the player's timestamp."""
        if self.wins:
            winners_database.update_timestamp(self)

    @property
    def rank(self):
        """Return the player's rank on the server."""
