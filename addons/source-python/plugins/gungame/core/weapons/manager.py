# ../gungame/core/weapons/manager.py

"""Weapon order management."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from engines.server import queue_command_string
from hooks.exceptions import except_hooks
from listeners.tick import Delay

# GunGame
from . import gg_weapons_logger
from .default import create_default_weapon_orders
from .errors import WeaponOrderError
from .order import WeaponOrder
from ..config.weapon import order_file, order_randomize
from ..paths import GUNGAME_WEAPON_ORDER_PATH
from ..status import GunGameMatchStatus, GunGameStatus


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    '_WeaponOrderManager',
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
        """Initialize the object."""
        super().__init__()

        # Set the default attributes
        self._active = None
        self._order = None
        self.randomize = False
        self._delay = None
        self._print_delay = None

        # Create the default files
        create_default_weapon_orders()

    @property
    def active(self):
        """Return the current active order."""
        if self.randomize:
            return self[self._active].random_order
        return self[self._active]

    @property
    def max_levels(self):
        """Return the current weapon order's max levels."""
        return self.active.max_levels

    def get_weapon_orders(self):
        """Retrieve all weapon orders and store them in the dictionary."""
        for file in GUNGAME_WEAPON_ORDER_PATH.files('*.txt'):
            try:
                self[file.namebase] = WeaponOrder(file)
            except WeaponOrderError:
                # TODO: make this gungame specific
                except_hooks.print_exception()

        if not len(self):
            raise ValueError('No valid weapon order files found.')

    def set_start_convars(self):
        """Set all base ConVars on load."""
        self.set_active_weapon_order(order_file.get_string())
        self.set_randomize(order_randomize.get_bool())

    def set_active_weapon_order(self, value):
        """Set the weapon order to the given value."""
        if value == '0':
            return
        if value not in self:
            raise ValueError(
                'Invalid weapon order "{weapon_order}".'.format(
                    weapon_order=value,
                )
            )
        if self._active == value:
            return
        self._active = value
        if self.randomize:
            self[self._active].randomize_order()
        self.print_order()

    def set_randomize(self, value):
        """Set the randomize value and randomize the weapon order."""
        if not isinstance(value, bool):
            value = bool(int(value))
        if self.randomize == value:
            return
        self.randomize = value
        if value:
            self[self._active].randomize_order()
        self.restart_game()

    def print_order(self):
        """Delay 1 tick to print the current weapon order."""
        # Cancel the delay if it is active
        if self._print_delay is not None:
            self._print_delay.cancel()

        # Print the order in 1 tick
        self._print_delay = Delay(0.2, self._print_order)

    def _print_order(self):
        """Print the current weapon order."""
        # Reset the delay
        self._print_delay = None

        # Set the prefix
        prefix = '[GunGame]'

        # Log the weapon order name
        gg_weapons_manager_logger.log_message(
            '{prefix} Weapon order: {weapon_order}\n'.format(
                prefix=prefix,
                weapon_order=self.active.title,
            )
        )
        levels = list()
        multi_kills = list()
        weapons = list()
        for level in self.active:
            levels.append(level)
            multi_kills.append(self.active[level].multi_kill)
            weapons.append(self.active[level].weapon)
        level_length = max(len(str(max(levels))), len('Level')) + 2
        multi_kill_length = max(
            len(str(max(multi_kills))), len('multi_kill')
        ) + 2
        weapon_length = max([
            len(weapon) for weapon in weapons] + [len('Weapon')]) + 4
        joint = (
            '{prefix} +{level_length}+{multi_kill_length}+'
            '{weapon_length}+'.format(
                prefix=prefix,
                level_length='-' * level_length,
                multi_kill_length='-' * multi_kill_length,
                weapon_length='-' * weapon_length,
            )
        )
        gg_weapons_manager_logger.log_message(joint)
        gg_weapons_manager_logger.log_message(
            '{prefix} |{level_title}|{multi_kill_title}|'
            '{weapon_title}|'.format(
                prefix=prefix,
                level_title='Level'.center(level_length),
                multi_kill_title='multi_kill'.center(multi_kill_length),
                weapon_title='Weapon'.center(weapon_length),
            )
        )
        gg_weapons_manager_logger.log_message(joint)
        for level in self.active:
            current = self.active[level]
            gg_weapons_manager_logger.log_message(
                '{prefix} |{level}|{multi_kill}|{weapon} |'.format(
                    prefix=prefix,
                    level=str(level).center(level_length),
                    multi_kill=str(current.multi_kill).center(
                        multi_kill_length
                    ),
                    weapon=current.weapon.rjust(weapon_length - 1),
                )
            )
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
        from ..players.dictionary import player_dictionary
        player_dictionary.clear()

        # Restart the match
        queue_command_string('mp_restartgame 1')

weapon_order_manager = _WeaponOrderManager()
