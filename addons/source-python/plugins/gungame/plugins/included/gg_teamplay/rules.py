# ../gungame/plugins/included/gg_teamplay/rules.py

"""Creates the gg_teamplay rules."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.rules.instance import GunGameRules
from gungame.core.rules.strings import rules_translations

# Plugin
from .configuration import (
    count_grenade_kills, count_melee_kills, end_on_first_kill,
)
from .info import info


# =============================================================================
# >> RULES
# =============================================================================
teamplay_rules = GunGameRules(info.name)
teamplay_rules.title = 'TeamplayRules'
for _key, _value in rules_translations.items():
    if _key.startswith('TeamplayRules:Base:'):
        teamplay_rules.register_rule(
            name=_key,
            value=_value,
        )

for _token_name, _convar in (
    ('count_grenade_kills', count_grenade_kills),
    ('count_melee_kills', count_melee_kills),
    ('end_on_first_kill', end_on_first_kill),
):
    teamplay_rules.register_convar_token(
        token_name=_token_name,
        convar=_convar,
        convar_type='int',
    )
