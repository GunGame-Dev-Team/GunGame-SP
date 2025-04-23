# ../gungame/core/messages.py

"""Messaging functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from collections import defaultdict
from warnings import warn

# Source.Python
from colors import WHITE
from messages import (
    DialogMsg, HudDestination, HudMsg, HintText, KeyHintText, SayText2,
    TextMsg, VGUIMenu,
)
from paths import TRANSLATION_PATH
from translations.strings import LangStrings, TranslationStrings

# GunGame
from ..paths import GUNGAME_TRANSLATION_PATH


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    '_MessageManager',
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
        self._hooked_messages = defaultdict(list)
        self._hooked_prefixes = defaultdict(list)

        # Loop through all message translation files
        message_path = GUNGAME_TRANSLATION_PATH / 'messages'
        for file in message_path.walkfiles('*.ini'):
            # Skip all server-specific files
            if file.stem.endswith('_server'):
                continue

            # Get the current translations
            instance = LangStrings(
                file.replace(TRANSLATION_PATH, '')[1:~3]
            )

            # Loop through all translations in the current file
            for key, value in instance.items():

                # Verify that the name is unique
                if key in self:
                    warn(f'Translation key "{key}" already registered.')
                    continue

                # Add the translations to the dictionary
                self[key] = value

    def hook_message(self, message_name, callback):
        """Add a hook to the given message's callback list."""
        if not callable(callback):
            raise ValueError('Callback is not callable')

        if (
            message_name in self._hooked_messages and
            callback in self._hooked_messages[message_name]
        ):
            raise ValueError(
                f'Hook "{callback}" already registered for '
                f'message "{message_name}".'
            )

        self._hooked_messages[message_name].append(callback)

    def unhook_message(self, message_name, callback):
        """Remove callback from the given message's list."""
        if message_name not in self._hooked_messages:
            raise ValueError(f'Message "{message_name}" is not hooked.')

        if callback not in self._hooked_messages[message_name]:
            raise ValueError(
                f'Hook "{callback}" is not registered for '
                f'message "{message_name}".'
            )

        self._hooked_messages[message_name].remove(callback)

        if not self._hooked_messages[message_name]:
            del self._hooked_messages[message_name]

    def hook_prefix(self, message_prefix, callback):
        """Add a hook to the given message prefix's callback list."""
        if not callable(callback):
            raise ValueError('Callback is not callable')

        if (
            message_prefix in self._hooked_prefixes and
            callback in self._hooked_prefixes[message_prefix]
        ):
            raise ValueError(
                f'Hook "{callback}" already registered for '
                f'message prefix "{message_prefix}".'
            )

        self._hooked_prefixes[message_prefix].append(callback)

    def unhook_prefix(self, message_prefix, callback):
        """Remove callback from the given message prefix's list."""
        if message_prefix not in self._hooked_prefixes:
            raise ValueError(
                f'Message prefix "{message_prefix}" is not hooked.'
            )

        if callback not in self._hooked_prefixes[message_prefix]:
            raise ValueError(
                f'Hook "{callback}" is not registered for '
                f'message prefix "{message_prefix}".'
            )

        self._hooked_prefixes[message_prefix].remove(callback)

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
            users = (users,)

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
            users = (users,)

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
            users = (users,)

        # Send the message to the users
        TextMsg(message, HudDestination.CONSOLE).send(*users, **tokens)

    def hint_message(self, message='', *users, **tokens):
        """Send a hint message to the given players."""
        # Get the message to send
        message = self._get_message(message)

        # Is there no message?
        if message is None:
            return

        # Convert user index to a tuple
        if isinstance(users, int):
            users = (users,)

        # Send the message to the users
        HintText(message).send(*users, **tokens)

    # pylint: disable=too-many-arguments
    def hud_message(
        self, message='', x=-1.0, y=-1.0, color1=WHITE,
        color2=WHITE, effect=0, fade_in=0.0, fade_out=0.0,
        hold=4.0, fx_time=0.0, channel=0, *users, **tokens
    ):
        """Send a hud message to the given players."""
        # Get the message to send
        message = self._get_message(message)

        # Is there no message?
        if message is None:
            return

        # Convert user index to a tuple
        if isinstance(users, int):
            users = (users,)

        # Send the message to the users
        HudMsg(
            message, x, y, color1, color2, effect, fade_in, fade_out,
            hold, fx_time, channel,
        ).send(*users, **tokens)

    def keyhint_message(self, message='', *users, **tokens):
        """Send a keyhint message to the given players."""
        # Get the message to send
        message = self._get_message(message)

        # Is there no message?
        if message is None:
            return

        # Convert user index to a tuple
        if isinstance(users, int):
            users = (users,)

        # Send the message to the users
        KeyHintText(message).send(*users, **tokens)

    def motd_message(
        self, panel_type='2', title='',
        message='', visible=True, *users, **tokens
    ):
        """Send a motd message to the given players."""
        # Get the message to send
        message = self._get_message(message)

        # Is there no message?
        if message is None:
            return

        # Convert user index to a tuple
        if isinstance(users, int):
            users = (users,)

        # Set the sub keys values
        sub_keys = {'title': title, 'type': str(panel_type), 'msg': message}

        # Send the message to the users
        VGUIMenu('info', sub_keys, visible).send(*users, **tokens)

    def top_message(
        self, message='', color=WHITE, time=4, *users, **tokens
    ):
        """Send a toptext message to the given players."""
        # Get the message to send
        message = self._get_message(message)

        # Is there no message?
        if message is None:
            return

        # Convert user index to a tuple
        if isinstance(users, int):
            users = (users,)

        # Send the message to the users
        DialogMsg(message, color, time).send(*users, **tokens)

    def _get_message(self, message_name):
        """Get the message to send."""
        # Is the message a set of translations?
        if isinstance(message_name, TranslationStrings):
            return message_name

        if message_name not in self:
            return message_name

        for callback in self._hooked_messages.get(message_name, []):
            if callback(message_name) is False:
                return None
        for message_prefix in self._hooked_prefixes:
            if not message_name.startswith(message_prefix):
                continue
            for callback in self._hooked_prefixes[message_prefix]:
                if callback(message_name, message_prefix) is False:
                    return None
        return self[message_name]


message_manager = _MessageManager()
