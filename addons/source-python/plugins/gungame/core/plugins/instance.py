# ../gungame/core/plugins/instance.py

"""Provides a plugin instance class."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from plugins.instance import LoadedPlugin
from gungame.core.plugins import gg_plugins_logger


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
