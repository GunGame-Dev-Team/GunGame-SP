# ../gungame/plugins/included/gg_random_spawn/__init__.py

"""Provides functions to get and set locations for spawn points."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from core import GAME_NAME
from entities.entity import BaseEntity, Entity
from filters.entities import BaseEntityIter, EntityIter


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
if GAME_NAME == 'csgo':
    def get_locations(class_name):
        for base_entity in BaseEntityIter(class_name):
            yield (
                base_entity.get_key_value_vector('origin'),
                base_entity.get_key_value_vector('angles'),
            )


    def set_location(class_name, origin, angles):
        base_entity = BaseEntity.create(class_name)
        base_entity.set_key_value_vector('origin', origin)
        base_entity.set_key_value_vector('angles', angles)


else:
    def get_locations(class_name):
        for entity in EntityIter(class_name):
            yield entity.origin, entity.angles


    def set_location(class_name, origin, angles):
        entity = Entity.create(class_name)
        entity.origin = origin
        entity.angles = angles


def remove_locations(class_name):
    for base_entity in BaseEntityIter(class_name):
        base_entity.remove()
