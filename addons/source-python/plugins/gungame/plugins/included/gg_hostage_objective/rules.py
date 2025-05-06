# ../gungame/plugins/included/gg_hostage_objective/rules.py

"""Creates the gg_hostage_objective rules."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.rules.instance import GunGameRules

# Plugin
from .configuration import (
    killed_count,
    killed_levels,
    rescued_count,
    rescued_levels,
    stopped_count,
    stopped_levels,
)
from .info import info

# =============================================================================
# >> RULES
# =============================================================================
hostage_objective_rules = GunGameRules(info.name)
hostage_objective_rules.register_convar_token(
    token_name="killed_count",
    convar=killed_count,
)
hostage_objective_rules.register_convar_token(
    token_name="killed_levels",
    convar=killed_levels,
)
hostage_objective_rules.register_convar_token(
    token_name="rescued_count",
    convar=rescued_count,
)
hostage_objective_rules.register_convar_token(
    token_name="rescued_levels",
    convar=rescued_levels,
)
hostage_objective_rules.register_convar_token(
    token_name="stopped_count",
    convar=stopped_count,
)
hostage_objective_rules.register_convar_token(
    token_name="stopped_levels",
    convar=stopped_levels,
)
hostage_objective_rules.register_all_rules()
