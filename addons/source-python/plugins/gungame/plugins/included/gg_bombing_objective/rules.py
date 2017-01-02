# ../gungame/plugins/included/gg_bombing_objective/rules.py

"""Creates the gg_bombing_objective rules."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.rules.instance import GunGameRules
from gungame.core.rules.strings import rules_translations

# Plugin
from .configuration import defused_levels, detonated_levels
from .info import info


# =============================================================================
# >> RULES
# =============================================================================
bombing_objective_rules = GunGameRules(info.name)
bombing_objective_rules.title = 'BombingRules'
for _key, _value in rules_translations.items():
    if _key.startswith('BombingRules:'):
        bombing_objective_rules.register_rule(
            name=_key,
            value=_value,
        )

for _token_name, _convar in (
    ('defused_levels', defused_levels),
    ('detonated_levels', detonated_levels),
):
    bombing_objective_rules.register_convar_token(
        token_name=_token_name,
        convar=_convar,
        convar_type='int',
    )
