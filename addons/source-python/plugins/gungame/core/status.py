# ../gungame/core/status/__init__.py

"""GunGame status values."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Enum
from enum import IntEnum


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('GunGameStatus',
           'GunGameStatusType',
           )

# =============================================================================
# >> CLASSES
# =============================================================================
class GunGameStatusType(IntEnum):

    """Base Status values."""

    INACTIVE = 0
    ACTIVE = 1
    POST = 2
    ON_HOLD = 3


class GunGameStatus(object):

    """Stores statuses for GunGame."""

    # Set the base attributes all to False to start
    MATCH = LOADING = ROUND = GunGameStatusType.INACTIVE
