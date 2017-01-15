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
from players.entity import Player

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
    objectives = disable_type.get_int()

    # Do bombing objectives need removed?
    if objectives & ObjectiveType.BOMBING:

        # Disable bomb targets
        for entity in EntityIter('func_bomb_target'):
            entity.disable()

        # Remove all c4 entities
        for weapon in WeaponIter('objective'):
            weapon.remove()

    # Do hostage objectives need removed?
    if objectives & ObjectiveType.HOSTAGE:

        # Disable hostage rescue zones
        for entity in EntityIter('func_hostage_rescue'):
            entity.disable()

        # Remove all hostage entities
        for entity in EntityIter('hostage_entity'):
            entity.remove()
