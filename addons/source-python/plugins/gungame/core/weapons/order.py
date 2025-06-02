# ../gungame/core/weapons/order.py

"""Provides a weapon order based storage class."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from random import shuffle
from warnings import warn

# GunGame
from .errors import WeaponOrderError
from .groups import (
    all_weapons,
    machine_gun_weapons,
    other_primary_weapons,
    other_secondary_weapons,
    other_weapons,
    pistol_weapons,
    rifle_weapons,
    shotgun_weapons,
    smg_weapons,
    sniper_weapons,
)
from ..config.weapon import multi_kill_override

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "WeaponOrder",
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_multi_kill_weapons = (
    machine_gun_weapons | other_primary_weapons | other_secondary_weapons |
    other_weapons | pistol_weapons | rifle_weapons | shotgun_weapons |
    smg_weapons | sniper_weapons
)


# =============================================================================
# >> CLASSES
# =============================================================================
class WeaponOrder(dict):
    """Dictionary used to store a weapon order."""

    def __init__(self, file_path):
        """Store the values from the given path."""
        super().__init__()
        level = 0
        with file_path.open() as open_file:
            contents = open_file.read()

        for _line in contents.splitlines():
            line = _line.strip()
            if not line:
                continue
            if line.startswith("//"):
                continue
            values = line.split()
            if not values or len(values) > 2:  # noqa: PLR2004
                warn(
                    f'Invalid line "{line}" in weapon order file: '
                    f'{file_path.stem}',
                    stacklevel=2,
                )
            try:
                weapon, multi_kill = values
            except ValueError:
                weapon = values[0]
                multi_kill = 1
            try:
                multi_kill = int(multi_kill)
            except ValueError:
                warn(
                    f'Invalid multi-kill value "{multi_kill}" in weapon '
                    f'order file: {file_path.stem}',
                    stacklevel=2,
                )
                continue
            if weapon not in all_weapons:
                warn(
                    f'Invalid weapon "{weapon}" in weapon order file: '
                    f'{file_path.stem}',
                    stacklevel=2,
                )
                continue
            level += 1
            self[level] = _LevelWeapon(weapon, multi_kill)
        if not level:
            msg = (
                f'No valid lines found in weapon order file "{file_path.stem}".'
            )
            raise WeaponOrderError(msg)
        self.file_path = file_path
        self.name = self.file_path.stem
        self.title = self.name.replace("_", " ").title()
        self.random_order = None

    @property
    def max_levels(self):
        """Return the maximum number of levels for the weapon order."""
        return len(self)

    def randomize_order(self):
        """Get a randomized weapon order based on the instance."""
        self.random_order = {}
        randomize_weapons = list(self.values())
        keep_at_end = []
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
            self.random_order[level] = value


class _LevelWeapon:
    """Class used to store level specific values."""

    def __init__(self, weapon, multi_kill):
        """Store the base values."""
        self.weapon = weapon
        self._multi_kill = multi_kill

    @property
    def multi_kill(self):
        """Return the multi_kill value for the level."""
        override = int(multi_kill_override)
        if self.weapon in _multi_kill_weapons and override:
            return override
        return self._multi_kill
