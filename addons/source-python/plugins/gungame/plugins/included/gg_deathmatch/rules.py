# ../gungame/plugins/included/gg_deathmatch/rules.py

"""Creates the gg_deathmatch rules."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.rules.instance import GunGameRules
from gungame.core.rules.strings import rules_translations

# Plugin
from .configuration import delay
from .info import info


# =============================================================================
# >> RULES
# =============================================================================
deathmatch_rules = GunGameRules(info.name)
deathmatch_rules.title = 'DeathmatchRules'
for _key, _value in rules_translations.items():
    if _key.startswith('DeathmatchRules:'):
        deathmatch_rules.register_rule(
            name=_key,
            value=_value,
        )

for _token_name, _convar in (
    ('delay', delay),
):
    deathmatch_rules.register_convar_token(
        token_name=_token_name,
        convar=_convar,
        convar_type='float',
    )
