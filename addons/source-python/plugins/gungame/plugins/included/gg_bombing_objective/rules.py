# ../gungame/plugins/included/gg_bombing_objective/rules.py

"""Creates the gg_bombing_objective rules."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.rules.instance import GunGameRules

# Plugin
from .configuration import defused_levels, detonated_levels
from .info import info


# =============================================================================
# >> RULES
# =============================================================================
bombing_objective_rules = GunGameRules(info.name)
bombing_objective_rules.register_convar_token(
    token_name='defused_levels',
    convar=defused_levels,
)
bombing_objective_rules.register_convar_token(
    token_name='detonated_levels',
    convar=detonated_levels,
)
bombing_objective_rules.register_all_rules()
