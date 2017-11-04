# ../gungame/plugins/included/gg_ffa/games/csgo.py

"""CS:GO specific functionality for gg_ffa."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events import Event
from players.constants import HideHudFlags
from players.entity import Player


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_spawn')
def _player_spawn(game_event):
    """Disable radar for the spawning player."""
    Player.from_userid(game_event['userid']).hidden_huds |= HideHudFlags.RADAR
