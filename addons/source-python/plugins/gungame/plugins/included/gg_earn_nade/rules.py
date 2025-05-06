# ../gungame/plugins/included/gg_earn_nade/rules.py

"""Creates the gg_earn_nade rules."""

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
earn_nade_rules = GunGameRules(info.name)
earn_nade_rules.register_all_rules()
