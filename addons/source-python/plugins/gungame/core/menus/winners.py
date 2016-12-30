# ../gungame/core/menus/winners.py

"""Winner menu functionality."""


# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from players.entity import Player

# GunGame
from . import menu_strings
from ._rankings import get_winners_menu
from ..commands.registration import register_command_callback


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'send_winners_menu',
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
@register_command_callback('winners', menu_strings['Winners:Text'])
def send_winners_menu(index):
    """Send the winners menu to the player."""
    get_winners_menu(Player(index)).send(index)
