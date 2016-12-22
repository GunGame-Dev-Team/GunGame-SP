# ../gungame/core/plugins/instance.py

"""Provides a plugin instance class."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from plugins.instance import LoadedPlugin

# GunGame
from . import gg_plugins_logger


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'GGLoadedPlugin',
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_plugins_instance_logger = gg_plugins_logger.instance


# =============================================================================
# >> CLASSES
# =============================================================================
class GGLoadedPlugin(LoadedPlugin):
    """The GunGame plugin class."""

    logger = gg_plugins_instance_logger
