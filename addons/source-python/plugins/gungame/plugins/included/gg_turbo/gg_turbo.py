# ../gungame/plugins/included/gg_turbo/gg_turbo.py

"""Plugin that gives the next weapon immediately upon levelup."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from gungame.core.players.attributes import AttributePostHook


# =============================================================================
# >> ATTRIBUTE CALLBACKS
# =============================================================================
@AttributePostHook('level')
def _post_level_change(player, attribute, new_value, old_value):
    """Give the player their new weapon."""
    player.give_level_weapon()
