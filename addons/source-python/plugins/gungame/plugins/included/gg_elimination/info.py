# ../gungame/plugins/included/gg_elimination/info.py

"""Contains plugin information."""

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
info.name = 'gg_elimination'
info.title = 'GG Elimination'
info.author = 'GG Dev Team'
info.required = ['gg_dead_strip', 'gg_dissolver']
info.conflicts = ['gg_deathmatch', 'gg_teamplay', 'gg_teamwork']
