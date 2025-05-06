# ../gungame/plugins/included/gg_deathmatch/rules.py

"""Creates the gg_deathmatch rules."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.rules.instance import GunGameRules

# Plugin
from .configuration import delay
from .info import info

# =============================================================================
# >> RULES
# =============================================================================
deathmatch_rules = GunGameRules(info.name)
deathmatch_rules.register_convar_token(
    token_name="delay",
    convar=delay,
    convar_type="float",
)
deathmatch_rules.register_all_rules()
