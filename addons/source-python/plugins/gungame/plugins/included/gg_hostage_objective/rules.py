# ../gungame/plugins/included/gg_hostage_objective/rules.py

"""Creates the gg_hostage_objective rules."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.rules.instance import GunGameRules
from gungame.core.rules.strings import rules_translations

# Plugin
from .configuration import (
    killed_count, killed_levels, rescued_count, rescued_levels, stopped_count,
    stopped_levels,
)
from .info import info


# =============================================================================
# >> RULES
# =============================================================================
hostage_objective_rules = GunGameRules(info.name)
hostage_objective_rules.title = 'HostageRules'
for _key, _value in rules_translations.items():
    if _key.startswith('HostageRules:'):
        hostage_objective_rules.register_rule(
            name=_key,
            value=_value,
        )

for _token_name, _convar in (
    ('killed_count', killed_count),
    ('killed_levels', killed_levels),
    ('rescued_count', rescued_count),
    ('rescued_levels', rescued_levels),
    ('stopped_count', stopped_count),
    ('stopped_levels', stopped_levels),
):
    hostage_objective_rules.register_convar_token(
        token_name=_token_name,
        convar=_convar,
        convar_type='int',
    )
