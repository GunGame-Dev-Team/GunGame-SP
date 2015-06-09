# ../gungame/core/messages/manager.py

""""""

# =============================================================================
# >> IMPORTS
# =============================================================================
from colors import WHITE
from translations.strings import LangStrings
from gungame.core.paths import GUNGAME_TRANSLATION_PATH


# =============================================================================
# >> CLASSES
# =============================================================================
class _MessageManager(dict):

    """"""

    def __init__(self):
        """"""
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

    def center_message(users=None, message=''):
        """"""
        message = self._get_message(message)
        instance = TextMsg(
            destination=TextMsg.HUD_PRINTCENTER, message=message)
        instance.send(users or ())

    def chat_message(users=None, index=0, message=''):
        """"""
        message = self._get_message(message)
        instance = SayText2(index=index, message=message)
        instance.send(users or ())

    def echo_message(users=None, message=''):
        """"""
        message = self._get_message(message)
        instance = TextMsg(
            destination=TextMsg.HUD_PRINTCONSOLE, message=message)
        instance.send(users or ())

    def hint_message(users=None, message=''):
        """"""
        message = self._get_message(message)
        instance = HintText(message=message)
        instance.send(users or ())

    def hud_message(
            users=None, x=-1.0, y=-1.0, color1=WHITE, color2=WHITE, effect=0,
            fadein=0.0, fadeout=0.0, hold=4.0, fxtime=0.0, message=''):
        """"""
        message = self._get_message(message)
        instance = HudMsg(
            x=x, y=y, r1=color1.r, g1=color1.g, b1=color1.b, a1=color1.a,
            r2=color2.r, g2=color2.g, b2=color2.b, a2=color2.a,
            effect=effect, fadein=fadein, fadeout=fadeout,
            hold=hold, fxtime=fxtime, message=message)
        instance.send(users or ())

    def keyhint_message(users=None, message=''):
        """"""
        message = self._get_message(message)
        instance = KeyHintText(message=message)
        instance.send(users or ())

    def motd_message(
            users=None, panel_type=2, title='', message='', visible=True):
        """"""
        message = self._get_message(message)
        subkeys = {'title': title, 'type': panel_type, 'msg': message}
        instance = VGUIMenu(name='info', show=visible, subkeys=subkeys)
        instance.send(users or ())

    def top_message(users=None, message='', color=WHITE, time=4.0):
        """"""
        message = self._get_message(message)
        raise NotImplemented(
            'This feature is not yet implemented as an OOP class in SP')

    def _get_message(self, message):
        """"""
        # Is the message a set of translations?
        if isinstance(message, TranslationStrings):
            return message

        # Is the message a registered GunGame translation?
        if message in self:
            return self[message]

        # Return the string message
        return message

message_manager = _MessageManager()
