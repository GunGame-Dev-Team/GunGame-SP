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
__all__ = ('GunGameMatchStatus',
           'GunGameRoundStatus',
           'GunGameStatus',
           )


# =============================================================================
# >> CLASSES
# =============================================================================
class GunGameMatchStatus(IntEnum):

    """Match based status."""

    # GunGame is loading
    LOADING = -1

    # Match is ready to begin
    INACTIVE = 0

    # Match is on-going
    ACTIVE = 1

    # Warmup is on-going
    WARMUP = 2

    # Match is over, awaiting map change
    POST = 3

    # Some sub-plugin does not want leveling to occur
    CUSTOM = 4


class GunGameRoundStatus(IntEnum):

    """Round based status."""

    # Round is over, awaiting start of next round
    INACTIVE = 0

    # Round is currently going
    ACTIVE = 1


class GunGameStatus(object):

    """Stores statuses for GunGame."""

    # Set the base attributes to their start values
    MATCH = GunGameMatchStatus.LOADING
    ROUND = GunGameRoundStatus.INACTIVE
