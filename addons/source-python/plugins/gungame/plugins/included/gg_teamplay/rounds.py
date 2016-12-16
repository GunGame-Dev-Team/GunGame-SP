# ../gungame/plugins/included/gg_teamplay/rounds.py

"""Round-based teamplay functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events import Event

# Plugin
from .manager import team_dictionary


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('round_end')
def _increment_winning_team(game_event):
    winner = team_dictionary.get(game_event['winner'])
    if winner is None:
        return

    winner.increase_multi_kill()
