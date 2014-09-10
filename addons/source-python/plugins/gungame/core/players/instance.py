# ../gungame/core/players/instance.py

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Players
from players.helpers import index_from_userid
from players.helpers import uniqueid_from_playerinfo

# GunGame Imports
#   Players
from gungame.core.players.attributes import player_attributes


# =============================================================================
# >> CLASSES
# =============================================================================
class GunGamePlayer(PlayerEntity):
    '''Class used to interact directly with a specific player'''

    def __setattr__(self, attr, value):
        if attr in player_attributes and attr in attribute_hooks:
            if not attribute_hooks[attr].call_callbacks(self, value):
                return
        super(GunGamePlayer, self).__setattr__(attr, value)

    @property
    def level_multikill(self):
        return active_weapon_order[self.level].multikill

    @property
    def level_weapon(self):
        return active_weapon_order[self.level].weapon
