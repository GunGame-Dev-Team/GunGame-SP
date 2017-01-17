# ../gungame/plugins/included/gg_ffa/gg_ffa.py

"""Plugin that allows FreeForAll gameplay."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from entities import TakeDamageInfo
from entities.entity import Entity
from entities.hooks import EntityCondition, EntityPostHook, EntityPreHook
from memory import make_object
from players.entity import Player


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Store a variable to know whether to revert the team or not
_take_damage_dict = dict()


# =============================================================================
# >> HOOKED FUNCTIONS
# =============================================================================
@EntityPreHook(EntityCondition.is_bot_player, 'on_take_damage')
@EntityPreHook(EntityCondition.is_human_player, 'on_take_damage')
def _pre_take_damage(stack_data):
    """Change the victim's team if they are on the attacker's team."""
    take_damage_info = make_object(TakeDamageInfo, stack_data[1])
    attacker = Entity(take_damage_info.attacker)
    if attacker.classname != 'player':
        return

    victim = make_object(Entity, stack_data[0])
    if victim.team != attacker.team:
        return

    address = stack_data.registers.esp.address.address
    if address in _take_damage_dict:
        return

    _take_damage_dict[address] = (victim.index, victim.team)

    # Change the player's team by using the m_iTeamNum property
    victim.team = 5 - victim.team


@EntityPostHook(EntityCondition.is_bot_player, 'on_take_damage')
@EntityPostHook(EntityCondition.is_human_player, 'on_take_damage')
def _post_take_damage(stack_data, return_value):
    """Revert the victim's team if necessary."""
    address = stack_data.registers.esp.address.address
    if address not in _take_damage_dict:
        return

    index, team = _take_damage_dict.pop(address)
    Entity(index).team = team
