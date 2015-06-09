# ../gungame/core/messages.py

"""Messaging functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from warnings import warn

from colors import WHITE
from messages import HudMsg
from messages import HintText
from messages import KeyHintText
from messages import SayText2
from messages import TextMsg
from messages import VGUIMenu
from translations.strings import LangStrings
from translations.strings import TranslationStrings

from gungame.core.paths import GUNGAME_TRANSLATION_PATH


# =============================================================================
# >> CLASSES
# =============================================================================
class _MessageManager(dict):

    """Class used to send messages to players."""

    def __init__(self):
        """Retrieve all core translations and store them in the dictionary."""
        super(_MessageManager, self).__init__()
        for file in GUNGAME_TRANSLATION_PATH.joinpath('core').files():
            if file.namebase.endswith('_server'):
                continue
            instance = LangStrings('gungame/core/{0}'.format(file.namebase))
            for key, value in instance.items():
                if key in self:
                    warn('Translation key "{0}" already registered.'.format(
                        key))
                    continue
                self[key] = value

    def center_message(self, users=None, message=''):
        """Send a center message to the given players."""
        message = self._get_message(message)
        instance = TextMsg(
            destination=TextMsg.HUD_PRINTCENTER, message=message)
        instance.send(users or ())

    def chat_message(self, users=None, index=0, message=''):
        """Send a chat message to the given players."""
        message = self._get_message(message)
        instance = SayText2(index=index, message=message)
        instance.send(users or ())

    def echo_message(self, users=None, message=''):
        """Send an echo message to the given players."""
        message = self._get_message(message)
        instance = TextMsg(
            destination=TextMsg.HUD_PRINTCONSOLE, message=message)
        instance.send(users or ())

    def hint_message(self, users=None, message=''):
        """Send a hint message to the given players."""
        message = self._get_message(message)
        instance = HintText(message=message)
        instance.send(users or ())

    def hud_message(
            self, users=None, x=-1.0, y=-1.0, color1=WHITE,
            color2=WHITE, effect=0, fadein=0.0, fadeout=0.0,
            hold=4.0, fxtime=0.0, message=''):
        """Send a hud message to the given players."""
        message = self._get_message(message)
        instance = HudMsg(
            x=x, y=y, r1=color1.r, g1=color1.g, b1=color1.b, a1=color1.a,
            r2=color2.r, g2=color2.g, b2=color2.b, a2=color2.a,
            effect=effect, fadein=fadein, fadeout=fadeout,
            hold=hold, fxtime=fxtime, message=message)
        instance.send(users or ())

    def keyhint_message(self, users=None, message=''):
        """Send a keyhint message to the given players."""
        message = self._get_message(message)
        instance = KeyHintText(message=message)
        instance.send(users or ())

    def motd_message(
            self, users=None, panel_type=2, title='',
            message='', visible=True):
        """Send a motd message to the given players."""
        message = self._get_message(message)
        subkeys = {'title': title, 'type': panel_type, 'msg': message}
        instance = VGUIMenu(name='info', show=visible, subkeys=subkeys)
        instance.send(users or ())

    def top_message(self, users=None, message='', color=WHITE, time=4.0):
        """Send a toptext message to the given players."""
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
            return self[message]

        # Return the string message
        return message

# Get the _MessageManager instance
message_manager = _MessageManager()
