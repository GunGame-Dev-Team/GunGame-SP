# ../gungame/core/warmup.py

"""GunGame Warmup Round functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Itertools
from itertools import cycle
#    Random
from random import shuffle
#   Warnings
from warnings import warn

# Source.Python Imports
#   Engines
from engines.server import engine_server
#   Filters
from filters.players import PlayerIter
from filters.weapons import WeaponClassIter
#   Listeners
from listeners.tick import TickRepeat

# GunGame Imports
#   Config
from gungame.core.config.warmup import weapon as warmup_weapon
from gungame.core.config.warmup import time as warmup_time
from gungame.core.config.warmup import min_players
from gungame.core.config.warmup import max_extensions
from gungame.core.config.warmup import players_reached
from gungame.core.config.warmup import start_config
from gungame.core.config.warmup import end_config
#   Status
from gungame.core.status import GunGameMatchStatus
from gungame.core.status import GunGameStatus
#   Weapons
from gungame.core.weapons.manager import weapon_order_manager


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('warmup_manager',
           )

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Get all possible warmup weapons
_possible_weapons = set(
    [weapon.basename for weapon in WeaponClassIter('primary')])
_possible_weapons.update(
    [weapon.basename for weapon in WeaponClassIter('secondary')])
_possible_weapons.update(
    [weapon.basename for weapon in WeaponClassIter('explosive')])
if 'incendiary' in WeaponClassIter.filters:
    _possible_weapons.update(
        [weapon.basename for weapon in WeaponClassIter('incendiary')])

# Get a generator for human players
_human_nospec = PlayerIter('human', ['spec', 'un'])


# =============================================================================
# >> CLASSES
# =============================================================================
class _WarmupManager(object):
    """Class used to provide warmup functionality."""

    def __init__(self):
        """Store the base attributes."""
        self._repeat = TickRepeat(self._countdown)
        self._extensions = 0
        self._warmup_time = 0
        self._weapon = None
        self._weapon_cycle = None

    @property
    def repeat(self):
        """Return the warmup manager repeat."""
        return self._repeat

    @property
    def extensions(self):
        """Return the number of extensions used in warmup."""
        return self._extensions

    @property
    def warmup_time(self):
        """Return the length of the warmup round."""
        return self._warmup_time

    @property
    def weapon(self):
        """Return the warmup weapon."""
        return self._weapon

    @property
    def weapon_cycle(self):
        """Return the cycle of warmup weapons."""
        return self._weapon_cycle

    def set_warmup_weapon(self):
        """Set the warmup weapon(s)."""
        # Get the warmup weapon(s)
        current = warmup_weapon.get_string()

        # Is the value a specific weapon?
        if current in _possible_weapons:

            # Set the weapon cycle to include just the weapon
            self._weapon_cycle = cycle([current])
            return

        # Are all weapons supposed to be used at random?
        if current == 'random':

            # Set the weapon cycle to a randomized list of all weapons
            weapons = list(_possible_weapons)
            shuffle(weapons)
            self._weapon_cycle = cycle(weapons)
            return

        # Is the value a list of weapons?
        if ',' in current:

            # Store the weapons from the given list to the weapon cycle
            weapons = [weapon for weapon in current.split(
                ',') if weapon in _possible_weapons]
            if len(weapons):
                self._weapon_cycle = cycle(weapons)
                return

        # Store the weapon cycle as the first weapon in the active weapon order
        self._weapon_cycle = cycle([weapon_order_manager.active[1].weapon])

    def start_warmup(self):
        """Start warmup round."""
        # Reset the extensions used
        self._extensions = 0

        # Get the amount of time for warmup
        self._warmup_time = warmup_time.get_int()

        # Was an invalid value given?
        if self._warmup_time <= 0:
            warn(
                '"gg_warmup_time" is set to an invalid number.' +
                '  Skipping warmup round.')
            self.end_warmup()
            return

        # Get the configuration to call on warmup start
        current = start_config.get_string()

        # Is a configuration file supposed to be called?
        if current:

            # Call the start configuration
            engine_server.server_command('exec {0};'.format(current))

        # Get the warmup weapon
        self._find_warmup_weapon()

        # Set the match status
        GunGameStatus.MATCH = GunGameMatchStatus.WARMUP

        # TODO: Give warmup weapon

        # Start the warmup repeat
        self.repeat.start(1, self._warmup_time)

    @staticmethod
    def end_warmup():
        """End warmup and start the match."""
        # TODO: Call start match
        # Get the configuration to call on warmup end
        current = end_config.get_string()

        # Is a configuration file supposed to be called?
        if current:

            # Call the end configuration
            engine_server.server_command('exec {0};'.format(current))

    def _find_warmup_weapon(self):
        """Return the next weapon in the warmup cycle."""
        self._weapon = next(self.weapon_cycle)

    def _countdown(self):
        """Determine what to do once a second during warmup."""
        # Get the remaining time for warmup
        remaining = self.repeat.remaining

        # Is there no more time for the warmup?
        if not remaining:

            # End the warmup round
            self.end_warmup()
            return

        # Has the player limit been reached?
        if len(list(_human_nospec)) > min_players.get_int():

            # Get what to do when the player limit is reached
            current = players_reached.get_int()

            # Should warmup end?
            if current == 2 or (
                    self.extensions and current == 1):

                # Cause warmup to end in 1 second
                self.repeat.reduce(self.repeat.remaining - 1)
                return

        # Is there just one second remaining in warmup?
        if remaining == 1:

            # Should warmup be extended?
            if self.extensions < max_extensions.get_int():

                # TODO: send message about the extension

                # Extend the warmup round
                self._extensions += 1
                self.repeat.extend(self._warmup_time)
                return

        # TODO: send message to players about remaining warmup time

        if remaining <= 5:
            # TODO: play a beeping sound to indicate warmup ending soon
            pass

# Get the _WarmupManager instance
warmup_manager = _WarmupManager()
