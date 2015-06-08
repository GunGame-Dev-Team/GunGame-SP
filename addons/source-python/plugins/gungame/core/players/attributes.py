# ../gungame/core/players/attributes.py

"""Player attribute functionality."""


# =============================================================================
# >> CLASSES
# =============================================================================
class _Attribute(object):

    """Class used to store an attribute with its default value."""

    def __init__(self, default):
        """Store the default value on instantiation."""
        self._default = default

    @property
    def default(self):
        """Return the default value of the attribute."""
        return self._default


class _PlayerAttributes(dict):

    """Dictionary class used to store player attributes for GunGame."""

    def __setitem__(self, item, value):
        """Verify the given values before setting the item."""
        # Is the attribute already in the dictionary?
        if item in self:

            # If not, raise an error
            raise ValueError(
                'Given attribute "{0}" is already registered'.format(item))

        # Is the value given an _Attribute instance?
        if not isinstance(value, _Attribute):

            # If not, raise an error
            raise TypeError(
                'Given value "{0}" is not an '
                '_Attribute instance'.format(value))

        # Add the item to the dictionary
        super(_PlayerAttributes, self).__setitem__(item, value)

    def register_attribute(self, attribute, default):
        """Store the attribute in the dictionary with its default value."""
        self[attribute] = _Attribute(default)

    def unregister_attribute(self, attribute):
        """Remove the attribute from the dictionary."""
        del self[attribute]

# Get the _PlayerAttributes instance
player_attributes = _PlayerAttributes()

# Register the core attributes
player_attributes.register_attribute('level', 1)
player_attributes.register_attribute('multikill', 0)
player_attributes.register_attribute('wins', 0)


class _AttributeHook(list):

    """Class that stores a list of callbacks for the attribute hook."""

    def __init__(self, attribute):
        """Store the attribute's name."""
        super(_AttributeHook, self).__init__()
        self.attribute = attribute

    def append(self, callback):
        """Verify the callback is not a member and is callable."""
        if callback in self:
            raise
        if not callable(callback):
            raise
        super(_AttributeHook, self).append(callback)

    def call_callbacks(self, player, value):
        """Call all callbacks for the hook."""
        return_value = True
        for callback in self:
            callback_value = callback(player, self.attribute, value)
            if callback_value is not None and not callback_value:
                return_value = False
        return return_value


class _AttributeHooks(dict):

    """Dictionary used to store attribute hooks by name."""

    def __missing__(self, attribute):
        """Add the attribute to the dictionary as a hook."""
        value = self[attribute] = _AttributeHook(attribute)
        return value

    def register_callback(self, attribute, callback):
        """Verify the callback befor adding it to the attribute's hooks."""
        if not callable(callback):
            raise
        self[attribute].append(callback)

    def unregister_callback(self, attribute, callback):
        """Verify the given values before removing the callback."""
        if attribute not in self:
            raise
        if callback not in self[attribute]:
            raise
        self[attribute].remove(callback)
        if not self[attribute]:
            del self[attribute]

attribute_hooks = _AttributeHooks()
