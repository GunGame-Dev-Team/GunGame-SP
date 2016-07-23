# ../gungame/core/messages.py

"""Messaging functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Collections
from collections import defaultdict
#   Warnings
from warnings import warn

# Source.Python Imports
#   Colors
from colors import WHITE
#   Messages
from messages import DialogMsg
from messages import HudMsg
from messages import HintText
from messages import KeyHintText
from messages import SayText2
from messages import TextMsg
from messages import VGUIMenu
#   Paths
from paths import TRANSLATION_PATH
#   Translations
from translations.strings import LangStrings
from translations.strings import TranslationStrings

# GunGame Imports
#   Paths
from .paths import GUNGAME_TRANSLATION_PATH


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('_MessageManager',
           'message_manager',
           )


# =============================================================================
# >> CLASSES
# =============================================================================
class _MessageManager(dict):
    """Class used to send messages to players."""

    def __init__(self):
        """Retrieve all core translations and store them in the dictionary."""
        # Initialize the dictionary
        super().__init__()

        # Create base dictionaries to store message hooks
        self._hooked_messages = defaultdict()
        self._hooked_prefixes = defaultdict()

        # Loop through all directories in the GunGame translations directory
        for folder in GUNGAME_TRANSLATION_PATH.dirs():

            # Loop through all translation files in the current directory
            for file in folder.files('*.ini'):

                # Skip all server-specific files
                if file.namebase.endswith('_server'):
                    continue

                # Get the current translations
                instance = LangStrings(
                    file.replace(TRANSLATION_PATH, '')[1:~3])

                # Loop through all translations in the current file
                for key, value in instance.items():

                    # Verify that the name is unique
                    if key in self:
                        warn(
                            'Translation key "{0}" already registered.'.format(
                                key))
                        continue

                    # Add the translations to the dictionary
                    self[key] = value

    def hook_message(self, message_name):
        """Add a hook to the given message's refcount."""
        self._hooked_messages[message_name] += 1

    def unhook_message(self, message_name):
        """Decrement the given message's refcount."""
        self._hooked_messages[message_name] -= 1
        if not self._hooked_messages[message_name]:
            del self._hooked_messages[message_name]

    def hook_prefix(self, message_prefix):
        """Add a hook to the given prefix's refcount."""
        self._hooked_prefixes[message_prefix] += 1

    def unhook_prefix(self, message_prefix):
        """Decrement the given prefix's refcount."""
        self._hooked_prefixes[message_prefix] -= 1
        if not self._hooked_prefixes[message_prefix]:
            del self._hooked_prefixes[message_prefix]

    def center_message(self, message='', *users, **tokens):
        """Send a center message to the given players."""
        # Get the message to send
        message = self._get_message(message)

        # Is there no message?
        if message is None:
            return

        # Convert user index to a tuple
        if isinstance(users, int):
            users = (users, )

        # Get a new instance for the message
        TextMsg(message).send(*users, **tokens)

    def chat_message(self, message='', index=0, *users, **tokens):
        """Send a chat message to the given players."""
        # Get the message to send
        message = self._get_message(message)

        # Is there no message?
        if message is None:
            return

        # Convert user index to a tuple
        if isinstance(users, int):
            users = (users, )

        # Send the message to the users
        SayText2(message, index).send(*users, **tokens)

    def echo_message(self, message='', *users, **tokens):
        """Send an echo message to the given players."""
        # Get the message to send
        message = self._get_message(message)

        # Is there no message?
        if message is None:
            return

        # Convert user index to a tuple
        if isinstance(users, int):
            users = (users, )

        # Send the message to the users
        TextMsg(message, TextMsg.CONSOLE).send(*users, **tokens)

    def hint_message(self, message='', *users, **tokens):
        """Send a hint message to the given players."""
        # Get the message to send
        message = self._get_message(message)

        # Is there no message?
        if message is None:
            return

        # Convert user index to a tuple
        if isinstance(users, int):
            users = (users, )

        # Send the message to the users
        HintText(message).send(*users, **tokens)

    def hud_message(
            self, message='', x=-1.0, y=-1.0, color1=WHITE,
            color2=WHITE, effect=0, fade_in=0.0, fade_out=0.0,
            hold=4.0, fx_time=0.0, channel=0, *users, **tokens):
        """Send a hud message to the given players."""
        # Get the message to send
        message = self._get_message(message)

        # Is there no message?
        if message is None:
            return

        # Convert user index to a tuple
        if isinstance(users, int):
            users = (users, )

        # Send the message to the users
        HudMsg(
            message, x, y, color1, color2, effect, fade_in, fade_out,
            hold, fx_time, channel).send(*users, **tokens)

    def keyhint_message(self, message='', *users, **tokens):
        """Send a keyhint message to the given players."""
        # Get the message to send
        message = self._get_message(message)

        # Is there no message?
        if message is None:
            return

        # Convert user index to a tuple
        if isinstance(users, int):
            users = (users, )

        # Send the message to the users
        KeyHintText(message).send(*users, **tokens)

    def motd_message(
            self, panel_type=2, title='',
            message='', visible=True, *users, **tokens):
        """Send a motd message to the given players."""
        # Get the message to send
        message = self._get_message(message)

        # Is there no message?
        if message is None:
            return

        # Convert user index to a tuple
        if isinstance(users, int):
            users = (users, )

        # Set the subkeys values
        subkeys = {'title': title, 'type': panel_type, 'msg': message}

        # Send the message to the users
        VGUIMenu('info', subkeys, visible).send(*users, **tokens)

    def top_message(
            self, message='', color=WHITE, time=4.0, *users, **tokens):
        """Send a toptext message to the given players."""
        # Get the message to send
        message = self._get_message(message)

        # Is there no message?
        if message is None:
            return

        # Convert user index to a tuple
        if isinstance(users, int):
            users = (users, )

        # Send the message to the users
        DialogMsg(message, color, time).send(*users, **tokens)

    def _get_message(self, message):
        """Get the message to send."""
        # Is the message a set of translations?
        if isinstance(message, TranslationStrings):
            return message

        # Is the message a registered GunGame translation?
        if message in self:
            if message in self._hooked_messages:
                return None
            for prefix in self._hooked_prefixes:
                if message.startswith(prefix):
                    return None
            return self[message]

        # Return the string message
        return message

# Get the _MessageManager instance
message_manager = _MessageManager()
