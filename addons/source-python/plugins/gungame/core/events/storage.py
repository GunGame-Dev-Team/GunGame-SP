# ../gungame/core/events/storage.py

"""Event storage functionality."""


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('_GGResourceList',
           'gg_resource_list',
           )


# =============================================================================
# >> CLASSES
# =============================================================================
class _GGResourceList(list):
    """Class used to store a list of all GunGame res files."""

    def append(self, resource):
        """Add the res file and write it."""
        super().append(resource)
        resource.write()

    def write(self):
        """Write all files in the list."""
        for resource in self:
            resource.write()

    def load_events(self):
        """Load all events from all res files."""
        for resource in self:
            resource.load_events()

# The singleton object of the _GGResourceList class.
gg_resource_list = _GGResourceList()
