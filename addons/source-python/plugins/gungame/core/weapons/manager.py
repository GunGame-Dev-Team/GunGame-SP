# ../gungame/core/weapons/manager.py

"""Weapon order management."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from engines.server import engine_server
from filters.weapons import WeaponClassIter
from listeners.tick import Delay

# GunGame
from ..config.weapon import order_file, order_randomize
from ..paths import GUNGAME_WEAPON_ORDER_PATH
from ..status import GunGameMatchStatus, GunGameStatus
from . import gg_weapons_logger
from .order import WeaponOrder


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

# Store the weapons by type
_primary_weapons = sorted(
    [
        weapon.basename for weapon in WeaponClassIter('primary')
    ]
)

_secondary_weapons = sorted(
    [
        weapon.basename for weapon in WeaponClassIter('secondary')
    ]
)

_explosive_weapons = sorted(
    [
        weapon.basename for weapon in WeaponClassIter('explosive')
        if weapon.basename not in _primary_weapons + _secondary_weapons
    ]
)

_melee_weapons = sorted(
    [
        weapon.basename for weapon in WeaponClassIter('melee')
    ]
)


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
        self._randomize = False
        self._delay = None
        self._print_delay = None

        # Create the default files
        self._create_default_order()
        self._create_short_order()

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
            raise ValueError(
                'Invalid weapon order "{0}".'.format(
                    value,
                )
            )
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
            '{0} Weapon order: {1}\n'.format(
                prefix,
                self.active.title,
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
        multi_kill_length = max(len(str(max(multi_kills))), len('multi_kill')) + 2
        weapon_length = max([
            len(weapon) for weapon in weapons] + [len('Weapon')]) + 4
        joint = '{0} +{1}+{2}+{3}+'.format(
            prefix,
            '-' * level_length,
            '-' * multi_kill_length,
            '-' * weapon_length,
        )
        gg_weapons_manager_logger.log_message(joint)
        gg_weapons_manager_logger.log_message(
            '{0} |{1}|{2}|{3}|'.format(
                prefix,
                'Level'.center(level_length),
                'multi_kill'.center(multi_kill_length),
                'Weapon'.center(weapon_length),
            )
        )
        gg_weapons_manager_logger.log_message(joint)
        for level in self.active:
            current = self.active[level]
            gg_weapons_manager_logger.log_message(
                '{0} |{1}|{2}|{3} |'.format(
                    prefix,
                    str(level).center(level_length),
                    str(current.multi_kill).center(multi_kill_length),
                    current.weapon.rjust(weapon_length - 1),
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
        engine_server.server_command('mp_restartgame 1')

    @staticmethod
    def _create_default_order():
        """Create the default weapon order file, if necessary."""
        default = GUNGAME_WEAPON_ORDER_PATH / 'default.txt'
        if default.isfile():
            return
        with default.open('w') as open_file:
            # TODO: print header
            for weapon in (
                _primary_weapons + _secondary_weapons +
                _explosive_weapons + _melee_weapons
            ):
                open_file.write(
                    '{0}\n'.format(
                        weapon,
                    )
                )

    @staticmethod
    def _create_short_order():
        """Create the short weapon order file, if necessary."""
        short = GUNGAME_WEAPON_ORDER_PATH / 'short.txt'
        if short.isfile():
            return
        with short.open('w') as open_file:
            # TODO: print header
            for weapon in _secondary_weapons:
                open_file.write(
                    '{0}\n'.format(
                        weapon,
                    )
                )

weapon_order_manager = _WeaponOrderManager()
