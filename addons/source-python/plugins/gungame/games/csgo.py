# ../gungame/games/csgo.py

"""CS:GO changes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame Imports
#   Messages
from gungame.core.messages import message_manager
#   Players
from gungame.core.players.weapons import _PlayerWeapons


# =============================================================================
# >> OVERRIDES
# =============================================================================
def _give_named_item(player, weapon):
    """Override for give_named_item to add other arguments."""
    player.give_named_item(weapon, 0, None, True)

# Set the override
_PlayerWeapons._give_named_item = _give_named_item


def _no_message(*args, **kwargs):
    """Override for messages that do not work."""
    ...

# Set the overrides
# TODO: Remove center/echo when TextMsg gets fixed
message_manager.center_message = _no_message
message_manager.echo_message = _no_message
message_manager.hud_message = _no_message
