# ../gungame/core/players/levels.py

"""Player level modification functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame Imports
#   Events
from gungame.core.events.included.leveling import GG_LevelDown
from gungame.core.events.included.leveling import GG_LevelUp
from gungame.core.events.included.match import GG_Win
#   Status
from gungame.core.status import GunGameStatus
from gungame.core.status import GunGameMatchStatus
#   Weapons
from gungame.core.weapons.manager import weapon_order_manager


# =============================================================================
# >> CLASSES
# =============================================================================
class _PlayerLevels(object):

    """Class used to interact with a player's level attribute."""

    def increase_level(self, levels, victim=0, reason=''):
        """Increase the player's level by the given amount."""
        if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
            return
        if levels < 1:
            raise ValueError()
        old_level = self.level
        new_level = old_level + levels
        if new_level > weapon_order_manager.max_levels:
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
        if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
            return
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
