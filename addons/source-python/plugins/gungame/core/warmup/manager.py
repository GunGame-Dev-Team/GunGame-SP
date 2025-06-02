# ../gungame/core/warmup/manager.py

"""GunGame Warmup Round functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from itertools import cycle
from random import shuffle
from warnings import warn

# Source.Python
from filters.players import PlayerIter
from listeners.tick import Repeat

# GunGame
from . import listeners
from ..config.warmup import (
    max_extensions,
    min_players,
    players_reached,
    warmup_time,
    warmup_weapon,
)
from ..messages.manager import message_manager
from ..sounds.manager import sound_manager
from ..status import GunGameMatchStatus, GunGameStatus
from ..weapons.groups import all_weapons, melee_weapons
from ..weapons.manager import weapon_order_manager

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "_WarmupManager",
    "warmup_manager",
)

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Get all possible warmup weapons
_possible_weapons = all_weapons - melee_weapons

# Get a generator for human players
_human_no_spec = PlayerIter("human", ["spec", "un"])

COUNTDOWN_THRESHOLD = 5
MINIMUM_PLAYERS = 2


# =============================================================================
# >> CLASSES
# =============================================================================
class _WarmupManager:
    """Class used to provide warmup functionality."""

    def __init__(self):
        """Store the base attributes."""
        self.repeat = Repeat(self.countdown, cancel_on_level_end=True)
        self.extensions = 0
        self.warmup_time = 0
        self.weapon = None
        self.weapon_cycle = None

    def set_warmup_weapon(self):
        """Set the warmup weapon(s)."""
        # Get the warmup weapon(s)
        current = str(warmup_weapon)

        # Is the value a specific weapon?
        if current in _possible_weapons:

            # Set the weapon cycle to include just the weapon
            self.weapon_cycle = cycle([current])
            return

        # Are all weapons supposed to be used at random?
        if current == "random":

            # Set the weapon cycle to a randomized list of all weapons
            weapons = list(_possible_weapons)
            shuffle(weapons)
            self.weapon_cycle = cycle(weapons)
            return

        # Is the value a list of weapons?
        if "," in current:

            # Store the weapons from the given list to the weapon cycle
            weapons = [
                weapon for weapon in current.split(
                    ",",
                ) if weapon in _possible_weapons
            ]
            if weapons:
                self.weapon_cycle = cycle(weapons)
                return

        # Store the weapon cycle as the first weapon in the active weapon order
        self.weapon_cycle = cycle([weapon_order_manager.active[1].weapon])

    def start_warmup(self):
        """Start warmup round."""
        if GunGameStatus.MATCH is GunGameMatchStatus.WARMUP:
            return
        self.extensions = 0
        self.warmup_time = int(warmup_time)

        # Was an invalid value given?
        if self.warmup_time <= 0:
            warn(
                '"gg_warmup_time" is set to an invalid number.'
                '  Skipping warmup round.',
                stacklevel=2,
            )
            self.end_warmup()
            return

        if self.weapon_cycle is None:
            self.set_warmup_weapon()

        # Get the warmup weapon
        self.get_current_warmup_weapon()

        # Set the match status
        GunGameStatus.MATCH = GunGameMatchStatus.WARMUP

        # Start the warmup repeat
        self.repeat.start(1, self.warmup_time)

        listeners.load()

    @staticmethod
    def end_warmup():
        """End warmup and start the match."""
        listeners.unload()
        from ..listeners import start_match
        GunGameStatus.MATCH = GunGameMatchStatus.INACTIVE
        start_match(ending_warmup=True)

    def get_current_warmup_weapon(self):
        """Return the next weapon in the warmup cycle."""
        self.weapon = next(self.weapon_cycle)

    def countdown(self):
        """Determine what to do once a second during warmup."""
        # Get the remaining time for warmup
        remaining = self.repeat.loops_remaining

        # Is there no more time for the warmup?
        if not remaining:

            # End the warmup round
            self.end_warmup()
            return

        # Has the player limit been reached?
        if len(list(_human_no_spec)) > int(min_players):

            # Get what to do when the player limit is reached
            current = int(players_reached)

            # Should warmup end?
            if (
                current == MINIMUM_PLAYERS or
                (self.extensions and current == 1)
            ):

                message_manager.center_message(
                    message="Warmup:Reduce",
                )

                # Cause warmup to end in 1 second
                self.repeat.reduce(self.repeat.loops_remaining - 1)
                return

        # Should warmup be extended?
        if remaining == 1 and self.extensions < int(max_extensions):
            message_manager.center_message(
                message="Warmup:Extend",
            )
            self.extensions += 1
            self.repeat.extend(self.warmup_time)
            return

        message_manager.center_message(
            message="Warmup:Countdown",
            seconds=remaining,
        )

        if remaining <= COUNTDOWN_THRESHOLD:
            sound_manager.play_sound("count_down")


warmup_manager = _WarmupManager()
