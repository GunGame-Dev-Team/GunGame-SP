# ../gungame/core/translations/strings.py

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
class GunGameLangStrings(LangStrings):

    """Class used to retrieve GunGame translations."""

    def __init__(self, name):
        """Add 'gungame' to the path prior to initialization."""
        infile = Path('gungame')
        try:
            folder = valid_plugins.get_plugin_type(name)
            infile = infile.joinpath(folder + '_plugins', name)
        except ValueError:
            infile = infile.joinpath(name)
        super(GunGameLangStrings, self).__init__(infile)
