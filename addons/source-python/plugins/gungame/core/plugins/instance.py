# ../gungame/core/plugins/instance.py

"""Provides a plugin instance class."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from plugins.instance import LoadedPlugin
from . import gg_plugins_logger


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_plugins_instance_logger = gg_plugins_logger.instance


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = ('GGLoadedPlugin',
           )


# =============================================================================
# >> CLASSES
# =============================================================================
class GGLoadedPlugin(LoadedPlugin):
    """The GunGame plugin class."""

    logger = gg_plugins_instance_logger
