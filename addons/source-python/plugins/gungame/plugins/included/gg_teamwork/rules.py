# ../gungame/plugins/included/gg_teamwork/rules.py

"""Creates the gg_teamwork rules."""

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
teamwork_rules = GunGameRules(info.name)
teamwork_rules.register_all_rules()
