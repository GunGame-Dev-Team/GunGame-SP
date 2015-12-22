from cvars import ConVar
from entities.entity import Entity
from events import Event


@Event('player_death')
def player_death(game_event):
    """"""
    entity = Entity.find_or_create('env_entity_dissolver')
    dissolve_type = ConVar('gg_dissolver_type').get_int()
    if dissolve_type not in range(4):
        dissolve_type = randint(0, 3)
    entity.dissolve_type = dissolve_type
    entity.magnitude = ConVar('gg_dissolver_magnitude').get_int()
    entity.dissolve('cs_ragdoll')
