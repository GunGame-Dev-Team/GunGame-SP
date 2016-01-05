# ../gungame/core/menus/winners.py

"""Winner menu functionality."""


# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Players
from players.entity import Player

# GunGame Imports
#   Menus
from gungame.core.menus._rankings import get_winners_menu


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def send_winners_menu(index):
    """Send the winners menu to the player."""
    get_winners_menu(Player(index)).send(index)
