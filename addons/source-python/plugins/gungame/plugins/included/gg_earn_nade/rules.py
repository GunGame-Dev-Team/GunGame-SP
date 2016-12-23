# ../gungame/plugins/included/gg_earn_nade/rules.py

"""Creates the gg_earn_nade rules."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.rules.instance import GunGameRules
from gungame.core.rules.strings import rules_translations

# Plugin
from .info import info


# =============================================================================
# >> RULES
# =============================================================================
earn_nade_rules = GunGameRules(info.name)
earn_nade_rules.title = 'EarnNadeRules'
for _key, _value in rules_translations.items():
    if _key.startswith('EarnNadeRules:'):
        earn_nade_rules.register_rule(
            name=_key,
            value=_value,
        )
