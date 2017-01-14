# ../gungame/plugins/included/gg_nade_bonus/gg_nade_bonus.py

"""Plugin to give extra weapons to players on nade levels."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events import Event

# Plugin
from .configuration import bonus_mode, bonus_reset, bonus_weapon


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('player_spawn')
def _stuff(game_event):
    pass


@Event('player_death')
def _stuff(game_event):
    pass


# =============================================================================
# >> GUNGAME EVENTS
# =============================================================================
@Event('gg_level_up')
def _stuff(game_event):
    pass


@Event('gg_level_down')
def _stuff(game_event):
    pass
