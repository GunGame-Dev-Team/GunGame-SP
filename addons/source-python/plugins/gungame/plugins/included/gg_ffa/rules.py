# ../gungame/plugins/included/gg_ffa/rules.py

"""Creates the gg_ffa rules."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.rules.instance import GunGameRules

# Plugin
from .info import info

# =============================================================================
# >> RULES
# =============================================================================
ffa_rules = GunGameRules(info.name)
ffa_rules.register_all_rules()
