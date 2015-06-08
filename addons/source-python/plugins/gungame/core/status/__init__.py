# ../gungame/core/status/__init__.py

"""GunGame status values."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Enum
from enum import IntEnum


# =============================================================================
# >> CLASSES
# =============================================================================
class GunGameStatus(IntEnum):

    """Base Status values."""

    INACTIVE = 0
    ACTIVE = 1
    POST = 2
    ON_HOLD = 3


class _GunGameStatus(object):

    """Stores statuses for GunGame."""

    # Set the base attributes all to False to start
    match = loading = round = GunGameStatus.INACTIVE

    def __setattr__(self, attribute, value):
        """Verify the attribute and value prior to setting."""
        # Is the given attribute a GunGame attribute?
        if not hasattr(self, attribute):

            # If not, raise an error
            raise AttributeError(
                'Cannot set attribute "{0}"'.format(attribute))

        # Is the given value a GunGameStatus value?
        if not isinstance(value, GunGameStatus):

            # If not, raise an error
            raise ValueError(
                'GunGameStatus attributes can only be set using ' +
                'GunGameStatus, not "{0}"'.format(type(value).__name__))

        # Set the attribute to the given value
        super(_GunGameStatus, self).__setattr__(attribute, value)

# Get the _GunGameStatus instance
gungame_status = _GunGameStatus()
