# ../gungame/addons/included/gg_deathmatch/__init__.py

"""Respawn players when they die."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Plugins
from plugins.info import PluginInfo


# =============================================================================
# >> PLUGIN INFO
# =============================================================================
info = PluginInfo()
info.name = 'gg_deathmatch'
info.title = 'GG Deathmatch'
info.author = 'GG Dev Team'
info.required = ['gg_dead_strip', 'gg_dissolver']
info.conflicts = ['gg_elimination', 'gg_teamplay', 'gg_teamwork']
info.translations = info.name
