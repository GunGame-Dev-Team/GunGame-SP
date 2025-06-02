# ../gungame/plugins/included/gg_dissolver/gg_dissolver.py

"""Plugin that dissolves player ragdolls on death."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from random import randrange
from warnings import warn

# Source.Python
from entities.constants import INVALID_ENTITY_INTHANDLE, DissolveType
from entities.entity import Entity
from entities.helpers import index_from_inthandle
from events import Event
from listeners.tick import Delay
from players.entity import Player

# GunGame
from gungame.core.status import GunGameMatchStatus, GunGameStatus

# Plugin
from .configuration import dissolver_delay, dissolver_type, magnitude

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_num_dissolve_types = len(DissolveType.__members__)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event("player_death")
def dissolve_player_ragdoll(game_event):
    """Dissolve/remove the player's ragdoll on death."""
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    # Get the type of dissolver to use
    current_type = int(dissolver_type)

    # Is the type valid?
    if current_type < 0 or current_type > _num_dissolve_types + 2:

        # Raise a warning
        warn(
            f'Invalid value for {dissolver_type.name} cvar "{current_type}".',
            stacklevel=2,
        )

        # Use the remove setting
        current_type = _num_dissolve_types + 2

    # Delay the dissolving
    Delay(
        delay=max(0, int(dissolver_delay)),
        callback=dissolve_ragdoll,
        args=(game_event["userid"], current_type),
        cancel_on_level_end=True,
    )


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def dissolve_ragdoll(userid, current_type):
    """Dissolve/remove the player's ragdoll."""
    # Get the ragdoll entity
    try:
        inthandle = Player.from_userid(userid).ragdoll
    except ValueError:
        return

    if inthandle == INVALID_ENTITY_INTHANDLE:
        return

    try:
        entity = Entity(index_from_inthandle(inthandle))
    except OverflowError:
        return

    # Should the ragdoll just be removed?
    if current_type == _num_dissolve_types + 2:
        entity.remove()
        return

    # Set the target name for the player's ragdoll
    entity.target_name = f"ragdoll_{userid}"

    # Get the dissolver entity
    dissolver_entity = Entity.find_or_create("env_entity_dissolver")

    # Should a random dissolve type be chosen?
    if current_type == _num_dissolve_types + 1:
        current_type = randrange(_num_dissolve_types)

    # Set the magnitude
    dissolver_entity.magnitude = int(magnitude)

    # Set the dissolve type
    dissolver_entity.dissolve_type = current_type

    # Dissolve the ragdoll
    dissolver_entity.dissolve(f"ragdoll_{userid}")
