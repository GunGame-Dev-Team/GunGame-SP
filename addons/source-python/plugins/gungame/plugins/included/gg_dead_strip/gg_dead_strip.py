# ../gungame/plugins/included/gg_dead_strip/gg_dead_strip.py

"""Plugin to strip weapons when a player dies."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events import Event

# GunGame
from gungame.core.weapons.helpers import remove_idle_weapons


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event("player_death")
def _strip_weapons(game_event):
    """Remove idle weapons when player dies."""
    remove_idle_weapons()
