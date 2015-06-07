# ../gungame/core/events/storage.py

""""""


# =============================================================================
# >> CLASSES
# =============================================================================
class GGResourceList(list):
    def append(self, resource):
        super(GGResourceList, self).append(resource)
        resource.write()

    def write(self):
        for resource in self:
            resource.write()

    def load_events(self):
        for resource in self:
            resource.load_events()

gg_resource_list = GGResourceList()
