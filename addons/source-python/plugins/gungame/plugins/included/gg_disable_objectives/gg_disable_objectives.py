# ../gungame/plugins/included/gg_disable_objectives/gg_disable_objectives.py

"""Plugin that disables the map objectives."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from cvars import ConVar
from events import Event
from filters.entities import EntityIter
from weapons.entity import WeaponEntity


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    """Disable objectives on load."""
    disable_objectives()


def unload():
    """Re-enable all objectives."""
    # Loop through all bomb targets
    for entity in EntityIter('func_bomb_target', return_types='entity'):

        # Enable the bomb target
        entity.enable()

    # Loop through all rescue zones
    for entity in EntityIter('func_hostage_rescue', return_types='entity'):

        # Enable the rescue zone
        entity.enable()


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event
def round_start(game_event):
    """Disable objectives each round."""
    disable_objectives()


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def disable_objectives():
    """Find out which objectives to disable and disable them."""
    # Get the objectives to disable
    objectives = ConVar('gg_disable_objectives').get_int()

    # Do bombing objectives need removed?
    if objectives in (1, 2):

        # Loop through all bomb targets
        for entity in EntityIter('func_bomb_target', return_types='entity'):

            # Disable the bomb target
            entity.disable()

        # Loop through all c4 entities
        for index in EntityIter('weapon_c4'):

            # Get the entity's instance
            entity = WeaponEntity(index)

            # Get the entity's owner
            owner = entity.current_owner

            # Does the entity have an owner?
            if owner is not None:

                # Force the owner to drop the entity
                owner.drop_weapon(entity, None, None)

            # Remove the entity from the server
            entity.remove()

    # Do hostage objectives need removed?
    if objectives in (1, 3):

        # Loop through all rescue zones
        for entity in EntityIter('func_hostage_rescue', return_types='entity'):

            # Disable the rescue zone
            entity.disable()

        # Loop through all hostage entities
        for entity in EntityIter('hostage_entity', return_types='entity'):

            # Remove the entity from the server
            entity.remove()
