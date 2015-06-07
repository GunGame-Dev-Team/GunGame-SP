# ../gungame/core/events/resource.py

""""""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Site-Package Imports
#   Path
from path import Path

# Source.Python Imports
#   Events
from events.resource import ResourceFile

# Script Imports
from gungame.core.events.storage import gg_resource_list


# =============================================================================
# >> CLASSES
# =============================================================================
class GGResourceFile(ResourceFile):
    def __init__(self, filepath, *events):
        super(GGResourceFile, self).__init__(
            Path('gungame').joinpath(filepath), *events)
        gg_resource_list.append(self)
