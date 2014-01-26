# ../gungame/core/translations/strings.py

# =============================================================================
# >> IMPORTS
# =============================================================================
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
    def __init__(self, name):
        infile = path('gungame')
        try:
            folder = ValidAddons.get_addon_type(name)
            infile = infile.joinpath(folder + '_addon_translations', name)
        except ValueError:
            infile = infile.joinpath(name)
        super(GunGameLangStrings, self).__init__(infile)
