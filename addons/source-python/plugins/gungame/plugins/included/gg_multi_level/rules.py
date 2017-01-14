# ../gungame/plugins/included/gg_multi_level/rules.py

"""Creates the gg_multi_level rules."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.rules.instance import GunGameRules

# Plugin
from .configuration import length, levels
from .info import info


# =============================================================================
# >> RULES
# =============================================================================
multi_level_rules = GunGameRules(info.name)
multi_level_rules.register_convar_token(
    token_name='length',
    convar=length,
)
multi_level_rules.register_convar_token(
    token_name='levels',
    convar=levels,
)
multi_level_rules.register_all_rules()
