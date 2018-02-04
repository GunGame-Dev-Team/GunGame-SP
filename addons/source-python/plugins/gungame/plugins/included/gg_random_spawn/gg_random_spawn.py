# ../gungame/plugins/included/gg_random_spawn/gg_random_spawn.py

"""Plugin that spawns players in random locations."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from warnings import warn

# Source.Python
from engines.server import global_vars
from listeners import OnLevelInit, OnLevelEnd
from listeners.tick import Delay
from mathlib import QAngle, Vector

# GunGame
from gungame.core.paths import GUNGAME_DATA_PATH

# Plugin
from .backups import spawn_point_backups
from .entities import spawn_entities
from .locations import remove_locations, set_location


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
SPAWN_POINT_PATH = GUNGAME_DATA_PATH / 'spawn_points'


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    """Store old spawn points and create the new ones on load."""
    _level_init(global_vars.map_name)


def unload():
    """Reset to the old spawn points on unload."""
    spawn_points_file = SPAWN_POINT_PATH / global_vars.map_name + '.txt'
    if spawn_points_file.isfile():
        spawn_point_backups.clear(restore=True)


# =============================================================================
# >> LISTENERS
# =============================================================================
@OnLevelInit
def _level_init(map_name):
    Delay(
        delay=0,
        callback=_create_spawn_points,
        args=(map_name,),
    )


def _create_spawn_points(map_name):
    spawn_points_file = SPAWN_POINT_PATH / map_name + '.txt'
    if not spawn_points_file.isfile():
        warn(f'No spawn point file found for "{map_name}".')
        return

    spawn_point_backups.store_backups()

    for class_name in spawn_entities:
        remove_locations(class_name)

    with spawn_points_file.open() as open_file:
        for num, line in enumerate(open_file.read().splitlines(), start=1):
            try:
                values = list(
                    map(
                        float,
                        line.split(),
                    )
                )
            except ValueError:
                warn(
                    f'Line {num} in spawn point file "{map_name}" is invalid.'
                )
                continue

            if len(values) != 6:
                warn(
                    f'Line {num} in spawn point file "{map_name}" is invalid.'
                )
                continue

            origin = Vector(*values[:3])
            angles = QAngle(*values[3:])
            for class_name in spawn_entities:
                set_location(class_name, origin, angles)


@OnLevelEnd
def _clear_backups():
    spawn_point_backups.clear()
