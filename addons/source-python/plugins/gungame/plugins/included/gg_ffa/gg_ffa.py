# ../gungame/plugins/included/gg_ffa/gg_ffa.py

"""Plugin that allows FreeForAll gameplay."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python
from contextlib import suppress
from importlib import import_module

# Source.Python
from core import GAME_NAME
from entities import TakeDamageInfo
from entities.entity import Entity
from entities.hooks import EntityCondition, EntityPostHook, EntityPreHook
from memory import make_object
from memory.hooks import use_pre_registers

# GunGame
from gungame.core.status import GunGameMatchStatus, GunGameStatus


# =============================================================================
# >> GAME SPECIFIC IMPORT
# =============================================================================
with suppress(ModuleNotFoundError):
    import_module(f'gungame.plugins.included.gg_ffa.games.{GAME_NAME}')


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
# Store a variable to know whether to revert the team or not
_take_damage_dict = {}


# =============================================================================
# >> HOOKED FUNCTIONS
# =============================================================================
@EntityPreHook(EntityCondition.is_bot_player, 'on_take_damage')
@EntityPreHook(EntityCondition.is_human_player, 'on_take_damage')
def _pre_take_damage(stack_data):
    """Change the victim's team if they are on the attacker's team."""
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        return

    take_damage_info = make_object(TakeDamageInfo, stack_data[1])
    attacker = Entity(take_damage_info.attacker)
    if attacker.classname != 'player':
        return

    victim = make_object(Entity, stack_data[0])
    if victim.team_index != attacker.team_index:
        return

    address = stack_data[0].address
    if address in _take_damage_dict:
        return

    _take_damage_dict[address] = (victim.index, victim.team_index)

    # Change the player's team by using the m_iTeamNum property
    victim.team_index = 5 - victim.team_index


@EntityPostHook(EntityCondition.is_bot_player, 'on_take_damage')
@EntityPostHook(EntityCondition.is_human_player, 'on_take_damage')
def _post_take_damage(stack_data, return_value):
    """Revert the victim's team if necessary."""
    with use_pre_registers(stack_data):
        address = stack_data[0].address

    if address not in _take_damage_dict:
        return

    index, team = _take_damage_dict.pop(address)
    Entity(index).team_index = team
