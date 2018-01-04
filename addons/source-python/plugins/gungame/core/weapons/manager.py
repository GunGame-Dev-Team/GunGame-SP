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
        self._restart_delay = None
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

        if not self:
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
            raise ValueError(f'Invalid weapon order "{value}".')
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
        """Print the current weapon order."""
        if GunGameStatus.MATCH != GunGameMatchStatus.ACTIVE:
            return

        if self._print_delay is not None:
            self._print_delay.cancel()
        self._print_delay = Delay(
            delay=0.1,
            callback=self._print_order,
        )

    def _print_order(self):
        """Print the current weapon order."""
        self._print_delay = None

        # Set the prefix
        prefix = '[GunGame]'

        # Log the weapon order name
        gg_weapons_manager_logger.log_message(
            f'{prefix} Weapon order: {self.active.title}\n'
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
        weapon_length = max(
            [len(weapon) for weapon in weapons] + [len('Weapon')]
        ) + 4
        joint = (
            f'{prefix} +{"-" * level_length}+{"-" * multi_kill_length}+'
            f'{"-" * weapon_length}+'
        )
        gg_weapons_manager_logger.log_message(joint)
        level_title = 'Level'.center(level_length)
        multi_kill_title = 'multi_kill'.center(multi_kill_length)
        weapon_title = 'Weapon'.center(weapon_length)
        gg_weapons_manager_logger.log_message(
            f'{prefix} |{level_title}|{multi_kill_title}|{weapon_title}|'
        )
        gg_weapons_manager_logger.log_message(joint)
        for level in self.active:
            current = self.active[level]
            level_display = str(level).center(level_length)
            multi_kill = str(current.multi_kill).center(multi_kill_length)
            weapon = current.weapon.rjust(weapon_length - 1)
            gg_weapons_manager_logger.log_message(
                f'{prefix} |{level_display}|{multi_kill}|{weapon} |'
            )
        gg_weapons_manager_logger.log_message(joint)

    def restart_game(self):
        """Restart the match."""
        if self._restart_delay is not None:
            self._restart_delay.cancel()
        self._restart_delay = Delay(
            delay=1,
            callback=self._restart_game,
        )

    def _restart_game(self):
        """Restart the match."""
        self._restart_delay = None

        GunGameStatus.MATCH = GunGameMatchStatus.INACTIVE

        # Clear the player dictionary
        from ..players.dictionary import player_dictionary
        player_dictionary.clear()

        # Restart the match
        queue_command_string('mp_restartgame 1')

weapon_order_manager = _WeaponOrderManager()
