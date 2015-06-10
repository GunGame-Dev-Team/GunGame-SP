# ../gungame/core/weapons/manager.py

"""Weapon order management."""

from contextlib import suppress

from cvars import ConVar
from events import Event
from gungame.core.paths import GUNGAME_CFG_PATH
from gungame.core.weapons.order import WeaponOrder


WEAPON_ORDER_PATH = GUNGAME_CFG_PATH.joinpath('weapon_orders')


class _WeaponOrderManager(dict):

    """Class used to store weapon orders."""

    def __init__(self):
        """Set the base attributes."""
        super(_WeaponOrderManager, self).__init__()
        self._active = None
        self._order = None
        self._randomize = False
        self.multikill = None

    @property
    def active(self):
        """Return the current active order."""
        if self.randomize:
            return self[self._active].random_order
        return self[self._active]

    @property
    def randomize(self):
        """Return whether or not to use a randomized weapon order."""
        return self._randomize

    @property
    def max_levels(self):
        """Return the current weapon order's max levels."""
        return self.active.max_levels

    def get_weapon_orders(self):
        """Retrieve all weapon orders and store them in the dictionary."""
        for file in WEAPON_ORDER_PATH.files():
            self[file.namebase] = WeaponOrder(file)

    def set_start_convars(self):
        """Set all base ConVars on load."""
        self.set_active_weapon_order(
            ConVar('gg_weapon_order_file').get_string())
        self.set_randomize(ConVar('gg_randomize_weapon_order').get_string())
        self.multikill = ConVar('gg_multikill_override').get_int()

    def set_active_weapon_order(self, value):
        """Set the weapon order to the given value."""
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
        """Set the randomize value and randomize the weapon order."""
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
        """Restart the match."""

weapon_order_manager = _WeaponOrderManager()


@Event
def server_cvar(game_event):
    """Set the weapon order value if the ConVar is for the weapon order."""
    cvarname = game_event.get_string('cvarname')
    cvarvalue = game_event.get_string('cvarvalue')
    if cvarname == 'gg_weapon_order_file':
        weapon_order_manager.set_active_weapon_order(cvarvalue)
    elif cvarname == 'gg_weapon_order_randomize':
        weapon_order_manager.set_randomize(cvarvalue)
    elif cvarname == 'gg_multikill_override':
        with suppress(ValueError):
            weapon_order_manager.multikill = int(cvarvalue)
