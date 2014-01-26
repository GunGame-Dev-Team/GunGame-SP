# ../gungame/core/status/__init__.py


# =============================================================================
# >> CLASSES
# =============================================================================
class _StatusTypes(object):
    '''Base Status values'''

    @property
    def INACTIVE(self):
        '''False value for statuses'''
        return False

    @property
    def ACTIVE(self):
        '''True value for statuses'''
        return True

# Get the _StatusTypes instance
StatusTypes = _StatusTypes()


class _GunGameStatus(object):
    '''Stores statuses for GunGame'''

    # Set the base attributes all to False to start
    Match = Loading = Round = False

    def __setattr__(self, attribute, value):
        '''Override __setattr__ to only allow proper
            attributes to be set to proper values'''

        # Is the given attribute a GunGame attribute?
        if not hasattr(self, attribute):

            # If not, raise an error
            raise AttributeError('Cannot set attribute "%s"' % attribute)

        # Is the given value a boolean?
        if not isinstance(value, bool):

            # If not, raise an error
            raise ValueError(
                'GunGameStatus attributes can only be ' +
                'set to booleans, not "%s"' % type(value).__name__)

        # Set the attribute to the given value
        super(_GunGameStatus, self).__setattr__(attribute, value)

# Get the _GunGameStatus instance
GunGameStatus = _GunGameStatus()
