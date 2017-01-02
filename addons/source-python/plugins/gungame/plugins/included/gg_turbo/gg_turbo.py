# ../gungame/plugins/included/gg_turbo/gg_turbo.py

"""Plugin that gives the next weapon immediately upon level-up."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.players.attributes import AttributePostHook

# Plugin
from .configuration import quick_switch


# =============================================================================
# >> ATTRIBUTE CALLBACKS
# =============================================================================
@AttributePostHook('level')
def _post_level_change(player, attribute, new_value, old_value):
    """Give the player their new weapon."""
    player.strip_weapons()
    player.give_level_weapon()
    if quick_switch.get_int():
        # TODO: fix this for snipers
        player.next_attack = 0
