# ../gungame/core/players/instance.py

# =============================================================================
# >> IMPORTS
# =============================================================================
from listeners.tick import tick_delays
from players.entity import PlayerEntity
from weapons.entity import WeaponEntity
from weapons.manager import weapon_manager
# GunGame Imports
#   Players
from gungame.core.players.attributes import attribute_hooks
from gungame.core.players.attributes import player_attributes
#   Weapons
from gungame.core.weapons.manager import weapon_order_manager

# =============================================================================
# >> CLASSES
# =============================================================================
class GunGamePlayer(PlayerEntity):

    """Class used to interact directly with a specific player"""

    def __setattr__(self, attr, value):
        if (attr in player_attributes and attr in attribute_hooks
                and hasattr(self, attr)):
            if not attribute_hooks[attr].call_callbacks(self, value):
                return
        print('1 - Setting', attr)
        super(GunGamePlayer, self).__setattr__(attr, value)

    @property
    def level_multikill(self):
        return weapon_order_manager.active[self.level].multikill

    @property
    def level_weapon(self):
        return weapon_order_manager.active[self.level].weapon

    def give_level_weapon(self):
        weapon = weapon_manager[self.level_weapon]
        for index in self.weapon_indexes():
            entity = WeaponEntity(index)
            if entity.classname == weapon.name:
                return
        for index in self.weapon_indexes():
            entity = WeaponEntity(index)
            if weapon_manager[entity.classname].slot == weapon.slot:
                entity.remove()
        tick_delays.delay(0, self.give_named_item, weapon.name, 0)
