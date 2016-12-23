# ../gungame/plugins/included/gg_knife_elite/rules.py

"""Creates the gg_knife_elite rules."""

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
knife_elite_rules = GunGameRules(info.name)
knife_elite_rules.title = 'KnifeEliteRules'
for _key, _value in rules_translations.items():
    if _key.startswith('KnifeEliteRules:'):
        knife_elite_rules.register_rule(
            name=_key,
            value=_value,
        )
