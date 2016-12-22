# ../gungame/plugins/included/gg_knife_elite/gg_knife_elite.py

"""Plugin that only allows knives for the rest of the round after level up."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events import Event

# GunGame
from gungame.core.players.dictionary import player_dictionary


# =============================================================================
# >> GUNGAME EVENTS
# =============================================================================
@Event('gg_level_up')
def _strip_weapons(game_event):
    player_dictionary[game_event['leveler']].strip_weapons(strip_grenades=True)
