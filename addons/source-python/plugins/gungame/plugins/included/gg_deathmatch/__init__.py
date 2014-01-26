# ../gungame/addons/included/gg_deathmatch/__init__.py

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Addons
from addons.info import AddonInfo


# =============================================================================
# >> ADDON INFO
# =============================================================================
info = AddonInfo()
info.name = 'gg_deathmatch'
info.title = 'GG Deathmatch'
info.author = 'GG Dev Team'
info.required = ['gg_dead_strip', 'gg_dissolver']
info.conflicts = ['gg_elimination', 'gg_teamplay', 'gg_teamwork']
info.translations = info.name
