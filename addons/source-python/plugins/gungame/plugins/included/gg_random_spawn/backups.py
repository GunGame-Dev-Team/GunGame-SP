# ../gungame/plugins/included/gg_random_spawn/backups.py

"""Stores the original spawn points to be re-used on unload."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Plugin
from .entities import spawn_entities
from .locations import get_locations, remove_locations, set_location

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "spawn_point_backups",
)


# =============================================================================
# >> CLASSES
# =============================================================================
class _OldSpawnPoint:
    """Stores an old spawn point location."""

    def __init__(self, class_name, origin, angles):
        """Store the spawn point's base attributes."""
        self.class_name = class_name
        self.origin = origin
        self.angles = angles

    def restore_spawn_point(self):
        """Restore the old spawn point."""
        set_location(self.class_name, self.origin, self.angles)


class _SpawnPointBackups(list):
    """Dictionary that holds all old spawn points."""

    def clear(self, restore=False):
        """Clear the dictionary and restore all old spawn points."""
        if restore:
            for class_name in spawn_entities:
                remove_locations(class_name)
            for location in self:
                location.restore_spawn_point()
        super().clear()

    def store_backups(self):
        """Store all current spawn points prior to removal."""
        for class_name in spawn_entities:
            for origin, angles in get_locations(class_name):
                self.append(
                    _OldSpawnPoint(
                        class_name=class_name,
                        origin=origin,
                        angles=angles,
                    ),
                )


spawn_point_backups = _SpawnPointBackups()
