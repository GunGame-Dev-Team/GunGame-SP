# ../gungame/plugins/included/gg_nade_bonus/rules.py

"""Creates the gg_nade_bonus rules."""

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
nade_bonus_rules = GunGameRules(info.name)
nade_bonus_rules.register_all_rules()
