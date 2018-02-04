# ../gungame/plugins/included/gg_random_spawn/locations.py

"""Provides functions to get and set locations for spawn points."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from entities.entity import BaseEntity
from filters.entities import BaseEntityIter


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'get_locations',
    'remove_locations',
    'set_location',
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def get_locations(class_name):
    """Return all current spawn points for the given class name."""
    for base_entity in BaseEntityIter(class_name):
        yield base_entity.origin, base_entity.angles


def set_location(class_name, origin, angles):
    """Create a spawn point at the given location."""
    base_entity = BaseEntity.create(class_name)
    base_entity.origin = origin
    base_entity.angles = angles


def remove_locations(class_name):
    """Remove all current spawn points for the given class name."""
    for base_entity in BaseEntityIter(class_name):
        base_entity.remove()
