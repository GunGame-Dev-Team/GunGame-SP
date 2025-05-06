# ../gungame/plugins/included/gg_knife_elite/rules.py

"""Creates the gg_knife_elite rules."""

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
knife_elite_rules = GunGameRules(info.name)
knife_elite_rules.register_all_rules()
