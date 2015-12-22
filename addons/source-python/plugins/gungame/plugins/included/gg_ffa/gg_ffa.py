# ../gungame/plugins/included/gg_ffa/gg_ffa.py

"""Plugin that allows FreeForAll gameplay."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Entities
from entities import TakeDamageInfo
from entities.entity import Entity
from entities.hooks import EntityPostHook
from entities.hooks import EntityPreHook
#   Memory
from memory import make_object


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Store a variable to know whether to revert the team or not
_revert_team = False


# =============================================================================
# >> HOOKED FUNCTIONS
# =============================================================================
@EntityPreHook('CCSPlayer', 'on_take_damage')
def pre_take_damage(args):
    """Change the victim's team if they are on the attacker's team."""
    global _revert_team

    # Get the TakeDamageInfo object
    take_damage_info = make_object(TakeDamageInfo, args[1])

    # Get the attacker's instance
    attacker = Entity(take_damage_info.attacker)

    # If the attacker is not a player, return
    if attacker.classname != 'player':
        return

    # Get the victim's instance
    victim = make_object(Entity, args[0])

    # If the players are not on the same team, return
    if victim.team != attacker.team:
        return

    # Set the revert variable to know that we need to revert
    _revert_team = True

    # Change the player's team by using the m_iTeamNum property
    victim.team = 5 - victim.team


@EntityPostHook(['cs_bot', 'player'], 'on_take_damage')
def post_take_damage(args, return_value):
    """Revert the victim's team if necessary."""
    global _revert_team

    # If the victim's team doesn't need reverted, return
    if not _revert_team:
        return

    # Get the victim's instance
    victim = make_object(Entity, args[0])

    # Revert the player's team by using the m_iTeamNum property
    victim.team = 5 - victim.team

    # Reset the revert variable
    _revert_team = False
