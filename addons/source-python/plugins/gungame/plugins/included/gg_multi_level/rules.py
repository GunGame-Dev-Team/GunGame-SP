# ../gungame/plugins/included/gg_multi_level/rules.py

"""Creates the gg_multi_level rules."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.rules.instance import GunGameRules
from gungame.core.rules.strings import rules_translations

# Plugin
from .configuration import length, levels
from .info import info


# =============================================================================
# >> RULES
# =============================================================================
multi_level_rules = GunGameRules(info.name)
multi_level_rules.title = 'MultiLevelRules'
for _key, _value in rules_translations.items():
    if _key.startswith('MultiLevelRules:'):
        multi_level_rules.register_rule(
            name=_key,
            value=_value,
        )

for _token_name, _convar in (
    ('length', length),
    ('levels', levels),
):
    multi_level_rules.register_convar_token(
        token_name=_token_name,
        convar=_convar,
        convar_type='int',
    )
