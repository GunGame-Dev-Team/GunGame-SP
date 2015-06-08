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
#   Addons
from gungame.core.addons.valid import ValidAddons


# =============================================================================
# >> CLASSES
# =============================================================================
class GunGameLangStrings(LangStrings):

    """Class used to retrieve GunGame translations."""

    def __init__(self, name):
        """Add 'gungame' to the path prior to initialization."""
        infile = Path('gungame')
        try:
            folder = ValidAddons.get_addon_type(name)
            infile = infile.joinpath(folder + '_addon_translations', name)
        except ValueError:
            infile = infile.joinpath(name)
        super(GunGameLangStrings, self).__init__(infile)
