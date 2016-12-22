# ../gungame/plugins/included/gg_teamplay/info.py

"""Contains plugin information."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from plugins.info import PluginInfo


# =============================================================================
# >> PLUGIN INFO
# =============================================================================
info = PluginInfo()
info.name = 'gg_teamplay'
info.title = 'GG TeamPlay'
info.author = 'GG Dev Team'
info.conflicts = [
    'gg_bombing_objective', 'gg_handicap', 'gg_hostage_objective',
    'gg_teamwork',
]
