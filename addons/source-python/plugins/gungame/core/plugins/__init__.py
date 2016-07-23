# ../gungame/core/plugins/__init__.py

"""Plugin based functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from translations.strings import LangStrings
from .. import gg_core_logger


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
gg_plugins_logger = gg_core_logger.plugins
_plugin_strings = LangStrings('_core/plugin_strings')
