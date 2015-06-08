# ../gungame/core/events/storage.py

"""Event storage functionality."""


# =============================================================================
# >> CLASSES
# =============================================================================
class GGResourceList(list):

    """Class used to store a list of all GunGame res files."""

    def append(self, resource):
        """Add the res file and write it."""
        super(GGResourceList, self).append(resource)
        resource.write()

    def write(self):
        """Write all files in the list."""
        for resource in self:
            resource.write()

    def load_events(self):
        """Load all events from all res files."""
        for resource in self:
            resource.load_events()

gg_resource_list = GGResourceList()
