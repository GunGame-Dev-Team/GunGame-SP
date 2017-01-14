# ../gungame/plugins/included/gg_knife_steal/rules.py

"""Creates the gg_knife_steal rules."""

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
knife_steal_rules = GunGameRules(info.name)
knife_steal_rules.register_all_rules()
