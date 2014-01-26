from path import Path
from events.resource import ResourceFile
from gungame.core.events.storage import GGResourceList


class GGResourceFile(ResourceFile):
    def __init__(self, filepath, *events):
        super(GGResourceFile, self).__init__(
            Path('gungame').joinpath(filepath), *events)
        GGResourceList.append(self)
