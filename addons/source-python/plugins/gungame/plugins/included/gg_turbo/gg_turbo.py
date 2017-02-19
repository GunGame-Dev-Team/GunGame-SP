# ../gungame/plugins/included/gg_turbo/gg_turbo.py

"""Plugin that gives the next weapon immediately upon level-up."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from listeners.tick import Delay
from players.helpers import userid_from_index

# GunGame
from gungame.core.players.attributes import AttributePostHook
from gungame.core.players.dictionary import player_dictionary
from gungame.core.weapons.groups import incendiary_weapons

# Plugin
from .configuration import multiple_kills, quick_switch


# =============================================================================
# >> ATTRIBUTE CALLBACKS
# =============================================================================
@AttributePostHook('level')
def _post_level_change(player, attribute, new_value, old_value):
    """Give the player their new weapon."""
    if not new_value or not old_value:
        return
    if multiple_kills.get_bool():
        _give_level_weapon(player.index)
    else:
        Delay(0, _give_level_weapon, (player.index, ))


def _give_level_weapon(index):
    try:
        userid = userid_from_index(index)
    except ValueError:
        return
    player = player_dictionary[userid]
    player.strip_weapons(
        not_filters={'grenade'},
        remove_incendiary=player.level_weapon in incendiary_weapons,
    )
    player.give_level_weapon()
    if quick_switch.get_bool():
        # TODO: fix this for snipers
        player.next_attack = 0
