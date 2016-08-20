# ../gungame/plugins/included/gg_disable_objectives/info.py

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
info.name = 'gg_disable_objectives'
info.title = 'GG Disable Objectives'
info.author = 'GG Dev Team'
info.conflicts = ['gg_bomb_objective', 'gg_hostage_objective']
