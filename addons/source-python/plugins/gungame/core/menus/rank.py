# ../gungame/core/menus/rank.py

"""Rank menu functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from players.entity import Player

# GunGame
from ._rankings import get_winners_menu
from ..commands.registration import register_command_callback

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "send_rank_menu",
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
@register_command_callback("rank", "Rank:Text")
def send_rank_menu(index):
    """Send the rank menu to the player."""
    player = Player(index)
    menu = get_winners_menu(player)
    menu.set_player_page(index, _get_player_page(menu, player))
    menu.send(index)


def _get_player_page(menu, player):
    """Get the page that the player is listed on."""
    for page_number in range(menu.page_count + 1):
        for option in menu._get_options(page_number):  # noqa: SLF001
            if option.value == player.uniqueid:
                return page_number
    return 1
