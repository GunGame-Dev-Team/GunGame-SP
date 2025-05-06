# ../gungame/core/weapons/helpers.py

"""Helper functions for weapons."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from filters.weapons import WeaponIter
from weapons.manager import weapon_manager

# GunGame
from gungame.core.config.misc import map_strip_exceptions
from gungame.core.status import GunGameMatchStatus, GunGameStatus

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "remove_idle_weapons",
)


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def remove_idle_weapons(status=GunGameMatchStatus.ACTIVE):
    """Remove all idle weapons from the map."""
    if GunGameStatus.MATCH is not status:
        return

    for weapon in WeaponIter(
        not_filters=[
            tag for tag in ("tool", "objective") if tag in weapon_manager.tags
        ],
    ):
        # Is the weapon currently owned by a player?
        if weapon.owner is not None:
            continue

        # Is the weapon not supposed to be removed?
        if weapon_manager[weapon.classname].basename in map_strip_exceptions:
            continue

        weapon.remove()
