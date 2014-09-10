# ../gungame/core/players/attributes.py


# =============================================================================
# >> CLASSES
# =============================================================================
class _Attribute(object):
    '''Class used to store an attribute with its default value'''

    def __init__(self, default):
        '''Stores the default value on instantiation'''
        self._default = default

    @property
    def default(self):
        '''Returns the default value of the attribute'''
        return self._default


class _PlayerAttributes(dict):
    '''Dictionary class used to store player attributes for GunGame'''

    def __setitem__(self, item, value):
        '''Override __setitem__ to verify the item is not in the
            dictionary and the value is an _Attribute instance'''

        # Is the attribute already in the dictionary?
        if item in self:

            # If not, raise an error
            raise ValueError(
                'Given attribute "%s" is already registered' % item)

        # Is the value given an _Attribute instance?
        if not isinstance(value, _Attribute):

            # If not, raise an error
            raise TypeError(
                'Given value "%s" is not an _Attribute instance' % value)

        # Add the item to the dictionary
        super(_PlayerAttributes, self).__setitem__(item, value)

    def register_attribute(self, attribute, default):
        '''Stores the attribute in the dictionary with its default value'''
        self[attribute] = _Attribute(default)

    def unregister_attribute(self, attribute):
        '''Removes the attribute from the dictionary'''
        del self[attribute]

# Get the _PlayerAttributes instance
player_attributes = _PlayerAttributes()

# Register the core attributes
player_attributes.register_attribute('level', 1)
player_attributes.register_attribute('multikill', 0)


class _AttributeHook(list):
    def __init__(self, name):
        self.name = name

    def append(self, callback):
        if callback in self:
            raise
        if not callable(callback):
            raise
        super(_AttributeHook, self).append(callback)

    def remove(self, callback):
        super(_AttributeHook, self).remove(callback)
        if not self:
            attribute_hooks[self.name]

    def call_callbacks(self, player, value):
        for callback in self:
            callback(player, self.name, value)


class _AttributeHooks(dict):
    def __missing__(self, item):
        value = self[item] = _AttributeHook(item)
        return value

attribute_hooks = _AttributeHooks()
