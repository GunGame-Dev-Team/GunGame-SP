# ../gungame/core/status/__init__.py

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Enum
from enum import Enum

# =============================================================================
# >> CLASSES
# =============================================================================
class GunGameStatusTypes(Enum):
    """Base Status values"""

    INACTIVE = False
    ACTIVE = True


class _GunGameStatus(object):
    """Stores statuses for GunGame"""

    # Set the base attributes all to False to start
    match = loading = round = GunGameStatusTypes.INACTIVE

    def __setattr__(self, attribute, value):
        """Override __setattr__ to only allow proper
            attributes to be set to proper values"""
        # Is the given attribute a GunGame attribute?
        if not hasattr(self, attribute):

            # If not, raise an error
            raise AttributeError(
                'Cannot set attribute "{0}"'.format(attribute))

        # Is the given value a boolean?
        if type(value) is not GunGameStatusTypes:

            # If not, raise an error
            raise ValueError(
                'GunGameStatus attributes can only be set using ' +
                'GunGameStatusTypes, not "{0}"'.format(type(value).__name__))

        # Set the attribute to the given value
        super(_GunGameStatus, self).__setattr__(attribute, value)

# Get the _GunGameStatus instance
gungame_status = _GunGameStatus()
