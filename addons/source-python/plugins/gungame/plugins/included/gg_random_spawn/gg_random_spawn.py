# ../gungame/plugins/included/gg_random_spawn/gg_random_spawn.py

"""Plugin that spawns players in random locations."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from contextlib import suppress
from warnings import warn

# Source.Python
from engines.server import global_vars
from listeners import OnLevelEnd, OnLevelInit
from listeners.tick import Delay
from mathlib import QAngle, Vector

# GunGame
from gungame.core.paths import GUNGAME_CFG_PATH

# Plugin
from .backups import spawn_point_backups
from .entities import spawn_entities
from .locations import remove_locations, set_location

# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
SPAWN_POINT_PATH = GUNGAME_CFG_PATH / "spawn_points"


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    """Store old spawn points and create the new ones on load."""
    _level_init()


def unload():
    """Reset to the old spawn points on unload."""
    spawn_points_file = SPAWN_POINT_PATH / global_vars.map_name + ".txt"
    if spawn_points_file.is_file():
        spawn_point_backups.clear(restore=True)


# =============================================================================
# >> CLASSES
# =============================================================================
class SpawnPointManager:
    """Manager for spawn point creation."""

    spawn_point_delay = None

    def level_init(self):
        """Wait 1 tick then try to create the new spawn points."""
        if self.spawn_point_delay is not None:
            with suppress(ValueError):
                self.spawn_point_delay.cancel()

        self.spawn_point_delay = Delay(
            delay=0,
            callback=self.create_spawn_points,
        )

    def create_spawn_points(self):
        """Store backups and create the new spawn points from file."""
        self.spawn_point_delay = None

        map_name = global_vars.map_name
        spawn_points_file = SPAWN_POINT_PATH / map_name + ".txt"
        if not spawn_points_file.is_file():
            warn(
                f'No spawn point file found for "{map_name}".',
                stacklevel=2,
            )
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
                        ),
                    )
                except ValueError:
                    warn(
                        f'Line {num} in spawn point file "{map_name}" is '
                        f'invalid.',
                        stacklevel=2,
                    )
                    continue

                if len(values) != 6:  # noqa: PLR2004
                    warn(
                        f'Line {num} in spawn point file "{map_name}" is '
                        f'invalid.',
                        stacklevel=2,
                    )
                    continue

                origin = Vector(*values[:3])
                angles = QAngle(*values[3:])
                for class_name in spawn_entities:
                    set_location(class_name, origin, angles)


spawn_point_manager = SpawnPointManager()


# =============================================================================
# >> LISTENERS
# =============================================================================
@OnLevelInit
def _level_init(map_name=None):
    spawn_point_manager.level_init()


@OnLevelEnd
def _clear_backups():
    spawn_point_backups.clear()
