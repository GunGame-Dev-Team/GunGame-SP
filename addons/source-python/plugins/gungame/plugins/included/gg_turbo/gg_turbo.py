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
from gungame.core.weapons.groups import incendiary_weapons, sniper_weapons

# Plugin
from .configuration import multiple_kills, quick_switch


# =============================================================================
# >> ATTRIBUTE CALLBACKS
# =============================================================================
@AttributePostHook("level")
def _post_level_change(player, attribute, new_value, old_value):
    """Give the player their new weapon."""
    if not new_value or not old_value:
        return
    if multiple_kills.get_bool():
        _give_level_weapon(player.index)
    else:
        Delay(
            delay=0,
            callback=_give_level_weapon,
            args=(player.index,),
        )


def _give_level_weapon(index):
    try:
        player = player_dictionary.from_index(index)
    except ValueError:
        return
    player.strip_weapons(
        not_filters={"grenade"},
        remove_incendiary=player.level_weapon in incendiary_weapons,
    )
    player.give_level_weapon()
    if quick_switch.get_bool():
        player.next_attack = 0.5 if player.level_weapon in sniper_weapons else 0
