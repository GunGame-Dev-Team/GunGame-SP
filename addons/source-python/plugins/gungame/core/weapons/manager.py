# ../gungame/core/weapons/manager.py

"""Weapon order management."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Cvar
from cvars import ConVar
#   Events
from events import Event

# GunGame Imports
#   Paths
from gungame.core.paths import GUNGAME_WEAPON_ORDER_PATH
#   Weapons
from gungame.core.weapons.order import WeaponOrder


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('weapon_order_manager',
           )


# =============================================================================
# >> CLASSES
# =============================================================================
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
        for file in GUNGAME_WEAPON_ORDER_PATH.files():
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
