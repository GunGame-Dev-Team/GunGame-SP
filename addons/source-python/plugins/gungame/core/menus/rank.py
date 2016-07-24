# ../gungame/core/menus/rank.py

"""Rank menu functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from players.entity import Player

# GunGame
from ._rankings import get_winners_menu


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
    """Get the page that the player is listed on."""
    for page_number in range(menu.page_count + 1):
        for option in menu._get_options(page_number):
            if option.value == player.unique_id:
                return page_number
    return 1
