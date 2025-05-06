# ../gungame/core/plugins/info.py

"""Provides a class to store sub-plugin info."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from plugins.info import PluginInfo

# Site-package
from configobj import ConfigObj

# GunGame
from ..paths import GUNGAME_PLUGINS_PATH


# =============================================================================
# >> CLASSES
# =============================================================================
class GunGamePluginInfo(PluginInfo):
    """Class used to store plugin info for GunGame sub-plugins."""

    def __init__(self, info_module):
        """Override __init__ to get the proper info."""
        path = info_module.split(".")
        if (
            not info_module.startswith("gungame.plugins.") or
            path[2] not in ("included", "custom") or
            len(path) != 5  # noqa: PLR2004
        ):
            msg = f"Invalid plugin path given: {info_module}"
            raise ValueError(msg)
        name = path[3]
        ini_file = GUNGAME_PLUGINS_PATH / path[2] / name / "info.ini"
        if not ini_file.is_file():
            msg = f"No info.ini file found for plugin {name}"
            raise ValueError(msg)
        ini = ConfigObj(ini_file)
        super().__init__(name, **ini)
