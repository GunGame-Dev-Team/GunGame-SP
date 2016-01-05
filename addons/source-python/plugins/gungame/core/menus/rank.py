# ../gungame/core/menus/rank.py

"""Rank menu functionality."""

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
def send_rank_menu(index):
    """Send the rank menu to the player."""
    player = Player(index)
    menu = get_winners_menu(player)
    menu.set_player_page(index, _get_player_page(menu, player))
    menu.send(index)


def _get_player_page(menu, player):
    """"""
    for page_number in range(menu.page_count + 1):
        for option in menu._get_options(page_number):
            if option.value == player.uniqueid:
                return page_number
    return 1