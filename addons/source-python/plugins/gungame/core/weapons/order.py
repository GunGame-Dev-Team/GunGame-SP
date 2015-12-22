# ../gungame/core/weapons/order.py

"""Provides a weapon order based storage class."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Random
from random import shuffle

# Source.Python Imports
#   Cvars
from cvars import ConVar
#   Filters
from filters.weapons import WeaponClassIter

# GunGame Imports
#   Weapons
from gungame.core.weapons.errors import WeaponOrderError


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('WeaponOrder',
           )


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_primary_weapons = [weapon.basename for weapon in WeaponClassIter('primary')]
_secondary_weapons = [
    weapon.basename for weapon in WeaponClassIter('secondary')]
_multikill_weapons = _primary_weapons + _secondary_weapons


# =============================================================================
# >> CLASSES
# =============================================================================
class WeaponOrder(dict):

    """Dictionary used to store a weapon order."""

    def __init__(self, filepath):
        """Store the values from the given path."""
        super(WeaponOrder, self).__init__()
        with filepath.open() as open_file:
            level = 0
            for line in open_file:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('//'):
                    continue
                try:
                    weapon, multikill = line.split()
                except ValueError:
                    weapon = line
                    multikill = 1
                try:
                    multikill = int(multikill)
                except ValueError:
                    raise WeaponOrderError()
                level += 1
                self[level] = _LevelWeapon(weapon, multikill)
        self._filepath = filepath
        self._name = self.filepath.namebase
        self._title = self.name.replace('_', ' ').title()
        self._random_order = None

    @property
    def name(self):
        """Return the weapon order's name."""
        return self._name

    @property
    def filepath(self):
        """Return the weapon order's file path."""
        return self._filepath

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
        randomize_weapons = self.values()
        keep_at_end = list()
        for weapon in reversed(randomize_weapons):
            if weapon.weapon in _multikill_weapons:
                break
            keep_at_end.append(weapon)
        if keep_at_end:
            keep_at_end = reversed(keep_at_end)
            randomize_weapons = randomize_weapons[:-len(keep_at_end)]
        shuffle(randomize_weapons)
        randomize_weapons.extend(keep_at_end)
        for level, value in enumerate(randomize_weapons, 1):
            self._random_order[level] = value


class _LevelWeapon(object):

    """Class used to store level specific values."""

    def __init__(self, weapon, multikill):
        """Store the base values."""
        self._weapon = weapon
        self._multikill = multikill

    @property
    def weapon(self):
        """Return the level's weapon."""
        return self._weapon

    @property
    def multikill(self):
        """Return the multikill value for the level."""
        override = ConVar('gg_multikill_override').get_int()
        if self.weapon in _multikill_weapons and override:
            return override
        return self._multikill
