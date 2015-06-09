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

    def center_message(self, message=''):
        """Send a center message to the player."""
        message_manager.center_message(self.index, message)

    def chat_message(self, index=0, message=''):
        """Send a chat message to the player."""
        message_manager.chat_message(self.index, index, message)

    def echo_message(self, message=''):
        """Send an echo message to the player."""
        message_manager.echo_message(self.index, message)

    def hint_message(self, message=''):
        """Send a hint message to the player."""
        message_manager.hint_message(self.index, message)

    def hud_message(
            self, x=-1.0, y=-1.0, color1=WHITE, color2=WHITE, effect=0,
            fadein=0.0, fadeout=0.0, hold=4.0, fxtime=0.0, message=''):
        """Send a hud message to the player."""
        message_manager.hud_message(
            self.index, x, y, color1, color2, effect,
            fadein, fadeout, hold, fxtime, message)

    def keyhint_message(self, message=''):
        """Send a keyhint message to the player."""
        message_manager.keyhint_message(self.index, message)

    def motd_message(self, panel_type=2, title='', message='', visible=True):
        """Send a motd message to the player."""
        message_manager.motd_message(
                self.index, panel_type, title, message, visible)

    def top_message(self, message='', color=WHITE, time=4.0):
        """Send a toptext message to the player."""
        message_manager.top_message(self.index, message, color, time)
