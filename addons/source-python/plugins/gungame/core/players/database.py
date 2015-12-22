# ../gungame/core/players/database.py

"""Stores winner information for all players."""

# =============================================================================
# >> IMPORTS
# =============================================================================


# =============================================================================
# >> CLASSES
# =============================================================================
class _WinsDatabase(object):
    """Database to store player wins."""

    def __init__(self):
        self.connection = connect(GUNGAME_DATA_PATH.joinpath('winners.db'))
        self.connection.text_factory = str
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS WINNERS (name varchar(31), """
            """uniqueid TEXT UNIQUE, wins INT DEFAULT 0, """
            """timestamp varchar(31), PRIMARY KEY (uniqueid DESC))""")
        self.cursor.execute('PRAGMA auto_vacuum FULL')
        self.commit()

    def commit(self):
        if self.connection.total_changes:
            self.connection.commit()

    def update_timestamp(self, player):
        self.cursor.execute(
            """UPDATE WINNERS SET name=?, timestamp=? WHERE uniqueid=?""",
            (player.name, 'strftime("%s", "now")', player.uniqueid))

winners_database = _WinsDatabase()


class _PlayerDatabase(object):
    """Player wins/ranks functionality."""

    def _get_wins(self):
        """"""
        return int(winners_database.select(
            'WINNERS', 'wins', 'where uniqueid = "{0}"'.format(
                self.uniqueid)) or 0)

    def _set_wins(self, value):
        """"""
        if self.is_fake_client():
            return
        if self.wins:
            pass
        else:
            pass

    wins = property(_get_wins, _set_wins, '')

    def update_timestamp(self):
        """"""
        if self.wins:
            winners_database.update_timestamp(player)

    @property
    def rank(self):
        """Return the player's rank on the server."""
