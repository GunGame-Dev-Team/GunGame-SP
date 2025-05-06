# ../gungame/plugins/included/gg_elimination/rules.py

"""Creates the gg_elimination rules."""

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
elimination_rules = GunGameRules(info.name)
elimination_rules.register_all_rules()
