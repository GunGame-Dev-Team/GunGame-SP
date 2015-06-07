from cvars import ConVar
from events import Event
from gungame.core.paths import GUNGAME_CFG_PATH
from gungame.core.weapons.order import WeaponOrder


WEAPON_ORDER_PATH = GUNGAME_CFG_PATH.joinpath('weapon_orders')


class _WeaponOrderManager(dict):
    def __init__(self):
        self._active = None
        self._order = None
        self._randomize = False
        self.multikill = None

    @property
    def active(self):
        """"""
        if self.randomize:
            return self[self._active].random_order
        return self[self._active]

    @property
    def order(self):
        """"""
        return self._order

    @property
    def randomize(self):
        """"""
        return self._randomize

    def get_weapon_orders(self):
        for file in WEAPON_ORDER_PATH.files():
            self[file.namebase] = WeaponOrder(file)

    def set_start_convars(self):
        self.set_active_weapon_order(
            ConVar('gg_weapon_order_file').get_string())
        self.set_randomize(ConVar('gg_randomize_weapon_order').get_string())
        self.multikill = ConVar('gg_multikill_override').get_int()

    def set_active_weapon_order(self, value):
        if value == '0':
            return
        if value not in self:
            raise ValueError('Invalid weapon order "{0}".'.format(value))
        if self._active == value:
            return
        self._active = value
        if self.randomize:
            self[self._active].randomize_order()
        self.restart_game()

    def set_randomize(self, value):
        try:
            value = bool(int(value))
        except ValueError:
            raise ValueError(
                'Invalid value for randomize "{0}".'.format(value))
        if self.randomize == value:
            return
        self._randomize = value
        if value:
            self[self._active].randomize_order()
        self.restart_game()

    def restart_game(self):
        ...

weapon_order_manager = _WeaponOrderManager()


@Event
def server_cvar(game_event):
    cvarname = game_event.get_string('cvarname')
    cvarvalue = game_event.get_string('cvarvalue')
    if cvarname == 'gg_weapon_order_file':
        weapon_order_manager.set_active_weapon_order(cvarvalue)
    elif cvarname == 'gg_weapon_order_randomize':
        weapon_order_manager.set_randomize(cvarvalue)
    elif cvarname == 'gg_multikill_override':
        with suppress(ValueError):
            weapon_order_manager.multikill = int(cvarvalue)
