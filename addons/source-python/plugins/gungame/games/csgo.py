# ../gungame/games/csgo.py

"""CS:GO changes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from warnings import warn

# Source.Python
from core import GAME_NAME

# GunGame
from ..core.messages import message_manager
from ..core.players.instance import GunGamePlayer


# =============================================================================
# >> OVERRIDES
# =============================================================================
def _give_named_item(player, weapon):
    """Override for give_named_item to add other arguments."""
    player.give_named_item(weapon, 0, None, True)

# Set the override
GunGamePlayer._give_named_item = _give_named_item


class _NoMessage(object):
    """Class used to hook non-supported message types."""

    def __init__(self, message_type):
        """Store the message type."""
        self.message_type = message_type

    def _message_hook(self, *args, **kwargs):
        """Override for messages that do not work."""
        warn(
            'Message type "{0}" not supported for game "{1}".'.format(
                self.message_type,
                GAME_NAME,
            )
        )

# Set the overrides
message_manager.hud_message = _NoMessage('HudMsg')._message_hook
message_manager.top_message = _NoMessage('DialogMsg')._message_hook
