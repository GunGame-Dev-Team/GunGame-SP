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
from gungame.core.messages import message_manager


# =============================================================================
# >> OVERRIDES
# =============================================================================
class _NoMessage(object):
    """Class used to hook non-supported message types."""

    def __init__(self, message_type):
        """Store the message type."""
        self.message_type = message_type

    def _message_hook(self, *args, **kwargs):
        """Override for messages that do not work."""
        warn(
            'Message type "{message_type}" not supported for '
            'game "{game_name}".'.format(
                message_type=self.message_type,
                game_name=GAME_NAME,
            )
        )

# Set the overrides
message_manager.hud_message = _NoMessage('HudMsg')._message_hook
message_manager.top_message = _NoMessage('DialogMsg')._message_hook
message_manager.center_message = message_manager.hint_message
