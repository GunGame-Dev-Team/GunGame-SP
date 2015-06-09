# ../gungame/core/plugins/strings.py

"""GunGame translations functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Path
from path import Path

# Source.Python Imports
#   Translations
from translations.strings import LangStrings

# GunGame Imports
#   Plugins
from gungame.core.plugins.valid import valid_plugins


# =============================================================================
# >> CLASSES
# =============================================================================
class PluginStrings(LangStrings):

    """Class used to retrieve GunGame sub-plugin translations."""

    def __init__(self, name):
        """Add 'gungame' and the plugin type to the path."""
        super(PluginStrings, self).__init__('gungame/{0}_plugins/{1}'.format(
            valid_plugins.get_plugin_type(name), name))
