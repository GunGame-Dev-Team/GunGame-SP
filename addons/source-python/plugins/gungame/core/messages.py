# ../gungame/core/messages.py

"""Messaging functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Collections
from collections import defaultdict
#   Contextlib
from contextlib import suppress
#   Warnings
from warnings import warn

# Source.Python Imports
#   Colors
from colors import WHITE
#   Messages
with suppress(ImportError):
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
from gungame.core.paths import GUNGAME_TRANSLATION_PATH


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('message_manager',
           )


# =============================================================================
# >> CLASSES
# =============================================================================
class _MessageManager(dict):

    """Class used to send messages to players."""

    def __init__(self):
        """Retrieve all core translations and store them in the dictionary."""
        super(_MessageManager, self).__init__()
        self._hooked_messages = defaultdict()
        self._hooked_prefixes = defaultdict()
        for file in GUNGAME_TRANSLATION_PATH.walkfiles('*.ini'):
            if file.namebase.endswith('_server'):
                continue
            instance = LangStrings(file.replace(TRANSLATION_PATH, '')[1:~3])
            for key, value in instance.items():
                if key in self:
                    warn('Translation key "{0}" already registered.'.format(
                        key))
                    continue
                self[key] = value
        for key in sorted(self):
            print(key)

    def hook_message(self, message_name):
        """"""
        self._hooked_messages[message_name] += 1

    def unhook_message(self, message_name):
        self._hooked_messages[message_name] -= 1
        if not self._hooked_messages[message_name]:
            del self._hooked_messages[message_name]

    def hook_prefix(self, message_prefix):
        """"""
        self._hooked_prefixes[message_prefix] += 1

    def unhook_prefix(self, message_prefix):
        self._hooked_prefixes[message_prefix] -= 1
        if not self._hooked_prefixes[message_prefix]:
            del self._hooked_prefixes[message_prefix]

    def center_message(self, users=None, message='', **tokens):
        """Send a center message to the given players."""
        message = self._get_message(message)
        if message is None:
            return
        if isinstance(users, int):
            users = (users, )
        instance = TextMsg(
            destination=TextMsg.HUD_PRINTCENTER, message=message, **tokens)
        instance.send(*(users or ()))

    def chat_message(self, users=None, index=0, message='', **tokens):
        """Send a chat message to the given players."""
        message = self._get_message(message)
        if message is None:
            return
        if isinstance(users, int):
            users = (users, )
        instance = SayText2(index=index, message=message, **tokens)
        instance.send(*(users or ()))

    def echo_message(self, users=None, message='', **tokens):
        """Send an echo message to the given players."""
        message = self._get_message(message)
        if message is None:
            return
        if isinstance(users, int):
            users = (users, )
        instance = TextMsg(
            destination=TextMsg.HUD_PRINTCONSOLE, message=message, **tokens)
        instance.send(*(users or ()))

    def hint_message(self, users=None, message='', **tokens):
        """Send a hint message to the given players."""
        message = self._get_message(message)
        if message is None:
            return
        if isinstance(users, int):
            users = (users, )
        instance = HintText(message=message, **tokens)
        instance.send(*(users or ()))

    def hud_message(
            self, users=None, x=-1.0, y=-1.0, color1=WHITE,
            color2=WHITE, effect=0, fadein=0.0, fadeout=0.0,
            hold=4.0, fxtime=0.0, message='', **tokens):
        """Send a hud message to the given players."""
        message = self._get_message(message)
        if message is None:
            return
        if isinstance(users, int):
            users = (users, )
        instance = HudMsg(
            x=x, y=y, r1=color1.r, g1=color1.g, b1=color1.b, a1=color1.a,
            r2=color2.r, g2=color2.g, b2=color2.b, a2=color2.a,
            effect=effect, fadein=fadein, fadeout=fadeout,
            hold=hold, fxtime=fxtime, message=message, **tokens)
        instance.send(*(users or ()))

    def keyhint_message(self, users=None, message='', **tokens):
        """Send a keyhint message to the given players."""
        message = self._get_message(message)
        if message is None:
            return
        if isinstance(users, int):
            users = (users, )
        instance = KeyHintText(message=message, **tokens)
        instance.send(*(users or ()))

    def motd_message(
            self, users=None, panel_type=2, title='',
            message='', visible=True, **tokens):
        """Send a motd message to the given players."""
        message = self._get_message(message)
        if message is None:
            return
        if isinstance(users, int):
            users = (users, )
        subkeys = {'title': title, 'type': panel_type, 'msg': message}
        instance = VGUIMenu(
            name='info', show=visible, subkeys=subkeys, **tokens)
        instance.send(*(users or ()))

    def top_message(
            self, users=None, message='', color=WHITE, time=4.0, **tokens):
        """Send a toptext message to the given players."""
        message = self._get_message(message)
        if message is None:
            return
        if isinstance(users, int):
            users = (users, )
        # message = self._get_message(message)
        raise NotImplementedError(
            'This feature is not yet implemented as an OOP class in SP')

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
