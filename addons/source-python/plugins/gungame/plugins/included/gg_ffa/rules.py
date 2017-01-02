# ../gungame/plugins/included/gg_ffa/rules.py

"""Creates the gg_ffa rules."""

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
ffa_rules = GunGameRules(info.name)
ffa_rules.title = 'FFARules'
for _key, _value in rules_translations.items():
    if _key.startswith('FFARules:'):
        ffa_rules.register_rule(
            name=_key,
            value=_value,
        )
