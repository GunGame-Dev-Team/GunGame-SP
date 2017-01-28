# ../gungame/plugins/included/gg_turbo/gg_turbo.py

"""Plugin that gives the next weapon immediately upon level-up."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from listeners.tick import Delay

# GunGame
from gungame.core.players.attributes import AttributePostHook
from gungame.core.players.dictionary import player_dictionary

# Plugin
from .configuration import multiple_kills, quick_switch


# =============================================================================
# >> ATTRIBUTE CALLBACKS
# =============================================================================
@AttributePostHook('level')
def _post_level_change(player, attribute, new_value, old_value):
    """Give the player their new weapon."""
    if not new_value:
        return
    if multiple_kills.get_bool():
        _give_level_weapon(player.userid)
    else:
        Delay(0, _give_level_weapon, (player.userid, ))


def _give_level_weapon(userid):
    player = player_dictionary[userid]
    player.strip_weapons()
    player.give_level_weapon()
    if quick_switch.get_bool():
        # TODO: fix this for snipers
        player.next_attack = 0
