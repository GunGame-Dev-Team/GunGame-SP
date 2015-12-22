# ../gungame/core/players/messages.py

"""Provides player messaging functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from colors import WHITE
# GunGame Imports
#   Messages
from gungame.core.messages import message_manager


# =============================================================================
# >> CLASSES
# =============================================================================
class _PlayerMessages(object):
    """Class used to send messages to a specific player."""

    def center_message(self, message='', **tokens):
        """Send a center message to the player."""
        message_manager.center_message(message, self.index, **tokens)

    def chat_message(self, message='', index=0, **tokens):
        """Send a chat message to the player."""
        message_manager.chat_message(message, index, self.index, **tokens)

    def echo_message(self, message='', **tokens):
        """Send an echo message to the player."""
        message_manager.echo_message(message, self.index, **tokens)

    def hint_message(self, message='', **tokens):
        """Send a hint message to the player."""
        message_manager.hint_message(message, self.index, **tokens)

    def hud_message(
            self, message='', x=-1.0, y=-1.0, color1=WHITE,
            color2=WHITE, effect=0, fade_in=0.0, fade_out=0.0,
            hold=4.0, fx_time=0.0, channel=0, **tokens):
        """Send a hud message to the player."""
        message_manager.hud_message(
            message, x, y, color1, color2, effect, fade_in,
            fade_out, hold, fx_time, channel, self.index, **tokens)

    def keyhint_message(self, message='', **tokens):
        """Send a keyhint message to the player."""
        message_manager.keyhint_message(message, self.index, **tokens)

    def motd_message(
            self, panel_type=2, title='', message='', visible=True, **tokens):
        """Send a motd message to the player."""
        message_manager.motd_message(
                panel_type, title, message, visible, self.index, **tokens)

    def top_message(self, message='', color=WHITE, time=4.0, **tokens):
        """Send a toptext message to the player."""
        message_manager.top_message(message, color, time, self.index, **tokens)
