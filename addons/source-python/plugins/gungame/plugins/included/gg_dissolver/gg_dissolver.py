# ../gungame/plugins/included/gg_dissolver/gg_dissolver.py

"""Plugin that issolves player ragdolls on death."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from random import randint

# Source.Python
from entities.entity import Entity
from events import Event

# Plugin
from .configuration import dissolver_type, magnitude


# =============================================================================
# >> EVENTS
# =============================================================================
@Event('player_death')
def _player_death(game_event):
    """Dissolve the player's ragdoll on death."""
    entity = Entity.find_or_create('env_entity_dissolver')
    current = dissolver_type.get_int()
    if current not in range(4):
        current = randint(0, 3)
    entity.dissolve_type = current
    entity.magnitude = magnitude.get_int()
    entity.dissolve('cs_ragdoll')
