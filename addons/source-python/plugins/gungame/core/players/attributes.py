# ../gungame/core/players/attributes.py

"""Player attribute functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from core import AutoUnload

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "AttributePostHook",
    "AttributePreHook",
    "_AttributeBase",
    "_AttributeHooks",
    "_PlayerAttributes",
    "attribute_post_hooks",
    "attribute_pre_hooks",
    "player_attributes",
)


# =============================================================================
# >> CLASSES
# =============================================================================
class _PlayerAttributes(dict):
    """Dictionary class used to store player attributes for GunGame."""

    def __setitem__(self, item, value):
        """Verify the given values before setting the item."""
        # Is the attribute already in the dictionary?
        if item in self:

            # If not, raise an error
            msg = f'Given attribute "{item}" is already registered'
            raise ValueError(msg)

        # Add the item to the dictionary
        super().__setitem__(item, value)

    def register_attribute(self, attribute, default):
        """Store the attribute in the dictionary with its default value."""
        self[attribute] = default

        # Add the attribute to existing players
        try:
            from .dictionary import player_dictionary
        except ImportError:
            return
        for player in player_dictionary.values():
            setattr(player, attribute, default)

    def unregister_attribute(self, attribute):
        """Remove the attribute from the dictionary."""
        del self[attribute]

        # Remove the attribute from existing players
        try:
            from .dictionary import player_dictionary
        except ImportError:
            return

        for player in player_dictionary.values():
            delattr(player, attribute)


player_attributes = _PlayerAttributes()

# Register the core attributes
player_attributes.register_attribute("level", 1)
player_attributes.register_attribute("multi_kill", 0)


class _AttributeHook(list):
    """Class that stores a list of callbacks for the attribute hook."""

    def __init__(self, attribute):
        """Store the attribute's name."""
        super().__init__()
        self.attribute = attribute

    def append(self, callback):
        """Verify the callback is not a member and is callable."""
        # Is the callback already registered?
        if callback in self:
            msg = "Callback already registered."
            raise ValueError(msg)

        # Is the callback not callable?
        if not callable(callback):
            msg = "Callback is not callable."
            raise TypeError(msg)

        # Add the callback to the list
        super().append(callback)

    def remove(self, callback):
        """Verify the given values before removing the callback."""
        # Is the callback registered?
        if callback not in self:
            msg = "Callback is not registered."
            raise ValueError(msg)

        # Remove the callback from the list
        super().remove(callback)

    def call_callbacks(self, player, *args):
        """Call all callbacks for the hook."""
        # Set the default return value
        return_value = True

        # Loop through all callbacks
        for callback in self:

            # Call the callback and get its return value
            callback_value = callback(player, self.attribute, *args)

            # Does the current callback want to block setting the attribute?
            if callback_value is not None and not callback_value:

                # Set the attribute to not be changed
                return_value = False

        # Return whether to block or continue the attribute change
        return return_value


class _AttributeHooks(dict):
    """Dictionary used to store attribute hooks by name."""

    def __missing__(self, attribute):
        """Add the attribute to the dictionary as a hook."""
        value = self[attribute] = _AttributeHook(attribute)
        return value

    def register_callback(self, attribute, callback):
        """Add the callback to the attribute's list."""
        self[attribute].append(callback)

    def unregister_callback(self, attribute, callback):
        """Verify the attribute before removing the callback."""
        # Is the attribute hooked?
        if attribute not in self:
            msg = f'Attribute "{attribute}" is not hooked.'
            raise ValueError(msg)

        # Remove the callback from the attribute's list
        self[attribute].remove(callback)

        # Are there anymore callbacks for the attribute?
        if not self[attribute]:

            # If no more callbacks, remove the attribute from the dictionary
            del self[attribute]


attribute_pre_hooks = _AttributeHooks()
attribute_post_hooks = _AttributeHooks()


class _AttributeBase(AutoUnload):
    """Decorator class used to register callbacks to an attribute."""

    def __init__(self, attribute):
        """Store the attribute."""
        self.attribute = attribute
        self.callback = None

    def __call__(self, callback):
        """Store the callback and register it to the attribute."""
        # Store the callback
        self.callback = callback

        # Register the callback to the attribute
        self.hook_instance.register_callback(self.attribute, self.callback)

    @property
    def hook_instance(self):
        """All subclasses must define this method."""
        msg = "hook_instance not defined for class."
        raise NotImplementedError(msg)

    def _unload_instance(self):
        """Unregister the callback from the attribute."""
        self.hook_instance.unregister_callback(self.attribute, self.callback)


class AttributePostHook(_AttributeBase):
    """Decorator class to register post callbacks to an attribute."""

    hook_instance = attribute_post_hooks


class AttributePreHook(_AttributeBase):
    """Decorator class to register pre callbacks to an attribute."""

    hook_instance = attribute_pre_hooks
