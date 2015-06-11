# ../gungame/core/players/instance.py

"""Player instance functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from players.entity import PlayerEntity
from weapons.entity import WeaponEntity
from weapons.manager import weapon_manager

# GunGame Imports
#   Events
from gungame.core.events.included.leveling import GG_LevelDown
from gungame.core.events.included.leveling import GG_LevelUp
from gungame.core.events.included.match import GG_Win
#   Players
from gungame.core.players.attributes import attribute_post_hooks
from gungame.core.players.attributes import attribute_pre_hooks
from gungame.core.players.attributes import player_attributes
from gungame.core.players.messages import _PlayerMessages
#   Status
from gungame.core.status import GunGameStatusType
from gungame.core.status import GunGameStatus
#   Weapons
from gungame.core.weapons.manager import weapon_order_manager


# =============================================================================
# >> CLASSES
# =============================================================================
class GunGamePlayer(PlayerEntity, _PlayerMessages, _PlayerDatabase):

    """Class used to interact directly with a specific player."""

    def __setattr__(self, attr, value):
        """Verify that the attribute's value should be set."""
        # Are there any pre-hooks for the attribute?
        if (attr in player_attributes and
                attr in attribute_pre_hooks and hasattr(self, attr)):

            # Do any of the pre-hooks block the setting of the attribute?
            if not attribute_pre_hooks[attr].call_callbacks(self, value):

                # Block the attribute from being set
                return

        # Are there any post-hooks for the attribute?
        if not (attr in player_attributes and hasattr(self, attr) and
                attr in attribute_post_hooks):

            # If not, simply set the attribute's value
            super(GunGamePlayer, self).__setattr__(attr, value)
            return

        # Get the value prior to setting
        old_value = getattr(self, attr)

        # Set the attribute's value
        super(GunGamePlayer, self).__setattr__(attr, value)

        # Call all of the attribute's post-hooks
        attribute_post_hooks[attr].call_callbacks(self, value, old_value)

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
        self.give_named_item(weapon.name, 0)

    def increase_level(self, levels, victim=0, reason=''):
        """Increase the player's level by the given amount."""
        if levels < 1:
            raise ValueError()
        old_level = self.level
        new_level = old_level + levels
        if new_level > weapon_order_manager.max_levels:
            if GunGameStatus.MATCH is GunGameStatusType.POST:
                return
            with GG_Win() as event:
                event.attacker = event.winner = self.userid
                event.userid = event.loser = victim
            return
        self.level = new_level
        if self.level != new_level:
            return
        self.multikill = 0
        with GG_LevelUp() as event:
            event.attacker = event.leveler = self.userid
            event.userid = event.victim = victim
            event.old_level = old_level
            event.new_level = new_level
            event.reason = reason

    def decrease_level(self, levels, attacker=0, reason=''):
        """Decrease the player's level by the given amount."""
        if levels < 1:
            raise ValueError()
        old_level = self.level
        new_level = max(old_level - levels, 1)
        if self.level == new_level:
            return
        self.level = new_level
        if self.level != new_level:
            return
        self.multikill = 0
        with GG_LevelDown() as event:
            event.attacker = attacker
            event.leveler = event.userid = self.userid
            event.old_level = old_level
            event.new_level = new_level
            event.reason = reason
