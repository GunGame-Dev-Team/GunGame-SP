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
teamplay_rules.register_convar_token(
    token_name='count_grenade_kills',
    convar=count_grenade_kills,
)
teamplay_rules.register_convar_token(
    token_name='count_melee_kills',
    convar=count_melee_kills,
)
teamplay_rules.register_convar_token(
    token_name='end_on_first_kill',
    convar=end_on_first_kill,
)
for _key, _value in rules_translations.items():
    if _key.startswith(f'{info.name}:Base:'):
        teamplay_rules.register_rule(
            name=_key,
            value=_value,
        )
