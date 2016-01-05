# ../gungame/core/weapons/manager.py

"""Weapon order management."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Engines
from engines.server import engine_server
#   Listeners
from listeners.tick import Delay

# GunGame Imports
#   Config
from gungame.core.config.weapon import order_file
from gungame.core.config.weapon import order_randomize
from gungame.core.config.weapon import multikill_override
#   Paths
from gungame.core.paths import GUNGAME_WEAPON_ORDER_PATH
#   Status
from gungame.core.status import GunGameMatchStatus
from gungame.core.status import GunGameStatus
#   Weapons
from gungame.core.weapons import gg_weapons_logger
from gungame.core.weapons.order import WeaponOrder


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('_WeaponOrderManager',
           'weapon_order_manager',
           )


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_weapons_manager_logger = gg_weapons_logger.manager


# =============================================================================
# >> CLASSES
# =============================================================================
class _WeaponOrderManager(dict):
    """Class used to store weapon orders."""

    def __init__(self):
        """Set the base attributes."""
        super().__init__()
        self._active = None
        self._order = None
        self._randomize = False
        self._delay = None
        self._print_delay = None

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
        self.set_active_weapon_order(order_file.get_string())
        self.set_randomize(order_randomize.get_bool())

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

    def set_randomize(self, value):
        """Set the randomize value and randomize the weapon order."""
        if self.randomize == value:
            return
        self._randomize = value
        if value:
            self[self._active].randomize_order()
        self.restart_game()

    def print_order(self):
        """Delay 1 tick to print the current weapon order."""
        # Cancel the delay if it is active
        if self._print_delay is not None:
            self._print_delay.cancel()

        # Print the order in 1 tick
        self._print_delay = Delay(0, self._print_order)

    def _print_order(self):
        """Print the current weapon order."""
        # Reset the delay
        self._print_delay = None

        # Set the prefix
        prefix = '[GunGame]'

        # Log the weapon order name
        gg_weapons_manager_logger.log_message(
            '{0} Weapon order: {1}\n'.format(prefix, self.active.title))
        levels = list()
        multikills = list()
        weapons = list()
        for level in self.active:
            levels.append(level)
            multikills.append(self.active[level].multikill)
            weapons.append(self.active[level].weapon)
        level_length = max(len(str(max(levels))), len('Level')) + 2
        multikill_length = max(len(str(max(multikills))), len('Multikill')) + 2
        weapon_length = max([
            len(weapon) for weapon in weapons] + [len('Weapon')]) + 4
        joint = '{0} +{1}+{2}+{3}+'.format(
            prefix, '-' * level_length,
            '-' * multikill_length, '-' * weapon_length)
        gg_weapons_manager_logger.log_message(joint)
        gg_weapons_manager_logger.log_message('{0} |{1}|{2}|{3}|'.format(
            prefix, 'Level'.center(level_length),
            'Multikill'.center(multikill_length),
            'Weapon'.center(weapon_length)))
        gg_weapons_manager_logger.log_message(joint)
        for level in self.active:
            current = self.active[level]
            gg_weapons_manager_logger.log_message('{0} |{1}|{2}|{3} |'.format(
                prefix, str(level).center(level_length),
                str(current.multikill).center(multikill_length),
                current.weapon.rjust(weapon_length - 1)))
        gg_weapons_manager_logger.log_message(joint)

    def restart_game(self):
        """Restart the match."""
        if self._delay is not None:
            self._delay.cancel()
        self._delay = Delay(1, self._restart_game)

    def _restart_game(self):
        """Restart the match."""
        self._delay = None

        GunGameStatus.MATCH = GunGameMatchStatus.INACTIVE

        # Clear the player dictionary
        from gungame.core.players.dictionary import player_dictionary
        player_dictionary.clear()

        # Restart the match
        engine_server.server_command('mp_restartgame 1')

weapon_order_manager = _WeaponOrderManager()
