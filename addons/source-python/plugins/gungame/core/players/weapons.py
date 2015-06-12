# ../gungame/core/players/weapons.py

"""Player weapon based functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Weapons
from weapons.entity import WeaponEntity
from weapons.manager import weapon_manager

# GunGame Imports
#   Weapons
from gungame.core.weapons.manager import weapon_order_manager


# =============================================================================
# >> CLASSES
# =============================================================================
class _PlayerWeapons(object):

    """Class used to perform weapon based functionalities with a player."""

    @property
    def level_multikill(self):
        """Return the multikill value for the player's current level."""
        return weapon_order_manager.active[self.level].multikill

    @property
    def level_weapon(self):
        """Return the player's current level weapon."""
        return weapon_order_manager.active[self.level].weapon

    def give_level_weapon(self):
        """Give the player the weapon of their current level."""
        weapon = weapon_manager[self.level_weapon]
        for index in self.weapon_indexes():
            entity = WeaponEntity(index)
            if entity.classname == weapon.name:
                return
        for index in self.weapon_indexes():
            entity = WeaponEntity(index)
            if weapon_manager[entity.classname].slot == weapon.slot:
                self.drop_weapon(entity, None, None)
                entity.remove()
        self._give_named_item(weapon.name)

    def _give_named_item(self, weapon):
        """"""
        self.give_named_item(weapon, 0)
