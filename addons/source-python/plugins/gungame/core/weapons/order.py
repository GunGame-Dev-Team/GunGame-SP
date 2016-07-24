# ../gungame/core/weapons/order.py

"""Provides a weapon order based storage class."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from random import shuffle

# Source.Python
from filters.weapons import WeaponClassIter

# GunGame
from ..config.weapon import multi_kill_override
from .errors import WeaponOrderError


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'WeaponOrder',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_primary_weapons = [
    weapon.basename for weapon in WeaponClassIter('primary')
]
_secondary_weapons = [
    weapon.basename for weapon in WeaponClassIter('secondary')
]
_multi_kill_weapons = _primary_weapons + _secondary_weapons


# =============================================================================
# >> CLASSES
# =============================================================================
class WeaponOrder(dict):
    """Dictionary used to store a weapon order."""

    def __init__(self, file_path):
        """Store the values from the given path."""
        super().__init__()
        with file_path.open() as open_file:
            level = 0
            for line in open_file:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('//'):
                    continue
                try:
                    weapon, multi_kill = line.split()
                except ValueError:
                    weapon = line
                    multi_kill = 1
                try:
                    multi_kill = int(multi_kill)
                except ValueError:
                    raise WeaponOrderError()
                level += 1
                self[level] = _LevelWeapon(weapon, multi_kill)
        self._file_path = file_path
        self._name = self.file_path.namebase
        self._title = self.name.replace('_', ' ').title()
        self._random_order = None

    @property
    def name(self):
        """Return the weapon order's name."""
        return self._name

    @property
    def file_path(self):
        """Return the weapon order's file path."""
        return self._file_path

    @property
    def title(self):
        """Return the weapon order's title."""
        return self._title

    @property
    def max_levels(self):
        """Return the maximum number of levels for the weapon order."""
        return len(self)

    @property
    def random_order(self):
        """Return the randomized weapon order."""
        return self._random_order

    def randomize_order(self):
        """Get a randomized weapon order based on the instance."""
        self._random_order = dict()
        randomize_weapons = list(self.values())
        keep_at_end = list()
        for weapon in reversed(randomize_weapons):
            if weapon.weapon in _multi_kill_weapons:
                break
            keep_at_end.append(weapon)
        if keep_at_end:
            keep_at_end.reverse()
            randomize_weapons = randomize_weapons[:-len(keep_at_end)]
        shuffle(randomize_weapons)
        randomize_weapons.extend(keep_at_end)
        for level, value in enumerate(randomize_weapons, 1):
            self._random_order[level] = value


class _LevelWeapon(object):
    """Class used to store level specific values."""

    def __init__(self, weapon, multi_kill):
        """Store the base values."""
        self._weapon = weapon
        self._multi_kill = multi_kill

    @property
    def weapon(self):
        """Return the level's weapon."""
        return self._weapon

    @property
    def multi_kill(self):
        """Return the multi_kill value for the level."""
        override = multi_kill_override.get_int()
        if self.weapon in _multi_kill_weapons and override:
            return override
        return self._multi_kill
