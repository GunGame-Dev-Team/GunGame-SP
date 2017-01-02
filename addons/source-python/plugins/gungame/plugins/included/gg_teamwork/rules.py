# ../gungame/plugins/included/gg_teamwork/rules.py

"""Creates the gg_teamwork rules."""

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
teamwork_rules = GunGameRules(info.name)
teamwork_rules.title = 'TeamworkRules'
for _key, _value in rules_translations.items():
    if _key.startswith('TeamworkRules:'):
        teamwork_rules.register_rule(
            name=_key,
            value=_value,
        )
