from entities.entity import Entity
from events import Event

from .configuration import dissolver_type
from .configuration import magnitude


@Event('player_death')
def player_death(game_event):
    """"""
    entity = Entity.find_or_create('env_entity_dissolver')
    current = dissolve_type.get_int()
    if current not in range(4):
        current = randint(0, 3)
    entity.dissolve_type = current
    entity.magnitude = magnitude.get_int()
    entity.dissolve('cs_ragdoll')
