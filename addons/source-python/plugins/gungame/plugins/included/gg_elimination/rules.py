# ../gungame/plugins/included/gg_elimination/rules.py

"""Creates the gg_elimination rules."""

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
elimination_rules = GunGameRules(info.name)
elimination_rules.title = 'EliminationRules'
for _key, _value in rules_translations.items():
    if _key.startswith('EliminationRules:'):
        elimination_rules.register_rule(
            name=_key,
            value=_value,
        )
