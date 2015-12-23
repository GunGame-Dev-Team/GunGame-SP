# ../gungame/core/events/resource.py

"""GunGame event resource file functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Site-Package Imports
#   Path
from path import Path

# Source.Python Imports
#   Events
from events.resource import ResourceFile

# GunGame Imports
from gungame.core.events.storage import gg_resource_list


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('GGResourceFile',
           )


# =============================================================================
# >> CLASSES
# =============================================================================
class GGResourceFile(ResourceFile):
    """Class used for GunGame res files."""

    def __init__(self, filepath, *events):
        """Add 'gungame' to the path before initialization."""
        super().__init__(Path('gungame').joinpath(filepath), *events)
        gg_resource_list.append(self)
