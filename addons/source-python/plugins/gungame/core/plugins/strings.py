# ../gungame/core/plugins/strings.py

"""GunGame translations functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from translations.strings import LangStrings

# GunGame
from .valid import valid_plugins


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'PluginStrings',
)


# =============================================================================
# >> CLASSES
# =============================================================================
class PluginStrings(LangStrings):
    """Class used to retrieve GunGame sub-plugin translations."""

    def __init__(self, name):
        """Add 'gungame' and the plugin type to the path."""
        super().__init__(
            'gungame/{0}_plugins/{1}'.format(
                valid_plugins.get_plugin_type(name),
                name,
            )
        )
