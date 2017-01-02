# ../gungame/plugins/included/gg_knife_steal/rules.py

"""Creates the gg_knife_steal rules."""

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
knife_steal_rules = GunGameRules(info.name)
knife_steal_rules.title = 'KnifeStealRules'
for _key, _value in rules_translations.items():
    if _key.startswith('KnifeStealRules:'):
        knife_steal_rules.register_rule(
            name=_key,
            value=_value,
        )
