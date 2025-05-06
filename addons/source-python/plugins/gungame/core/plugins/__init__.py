# ../gungame/core/plugins/__init__.py

"""Plugin based functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from translations.strings import LangStrings

# GunGame
from .. import gg_core_logger

# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    "gg_plugins_logger",
    "plugin_strings",
)


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_plugins_logger = gg_core_logger.plugins
plugin_strings = LangStrings("_core/plugin_strings")
