# ../gungame/plugins/included/gg_disable_objectives/gg_disable_objectives.py

"""Plugin that disables the map objectives."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from enum import IntEnum

# Source.Python
from events import Event
from filters.entities import EntityIter
from filters.weapons import WeaponIter

# Plugin
from .configuration import disable_type


# =============================================================================
# >> CONSTANTS
# =============================================================================
class ObjectiveType(IntEnum):
    """Class used for objective comparison."""

    BOMBING = 1
    HOSTAGE = 2


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    """Disable objectives on load."""
    _disable_objectives()


def unload():
    """Re-enable all objectives."""
    # Loop through all bomb targets
    for entity in EntityIter('func_bomb_target'):

        # Enable the bomb target
        entity.enable()

    # Loop through all rescue zones
    for entity in EntityIter('func_hostage_rescue'):

        # Enable the rescue zone
        entity.enable()


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('round_start')
def _disable_objectives(game_event=None):
    """Disable objectives each round."""
    # Get the objectives to disable
    objectives = disable_type.get_int()

    # Do bombing objectives need removed?
    if objectives & ObjectiveType.BOMBING:

        # Loop through all bomb targets
        for entity in EntityIter('func_bomb_target'):

            # Disable the bomb target
            entity.disable()

        # Loop through all c4 entities
        for weapon in WeaponIter('objective'):

            # Get the entity's owner
            owner = weapon.current_owner

            # Does the entity have an owner?
            if owner is not None:

                # Force the owner to drop the entity
                owner.drop_weapon(weapon, None, None)

            # Remove the entity from the server
            weapon.remove()

    # Do hostage objectives need removed?
    if objectives & ObjectiveType.HOSTAGE:

        # Loop through all rescue zones
        for entity in EntityIter('func_hostage_rescue'):

            # Disable the rescue zone
            entity.disable()

        # Loop through all hostage entities
        for entity in EntityIter('hostage_entity'):

            # Remove the entity from the server
            entity.remove()
