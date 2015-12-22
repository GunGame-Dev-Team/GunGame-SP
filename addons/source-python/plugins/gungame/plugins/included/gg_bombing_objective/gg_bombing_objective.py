# ../gungame/plugins/included/gg_bombing_objective/gg_bombing_objective.py

""""""

# =============================================================================
# >> IMPORTS
# =============================================================================
from contextlib import suppress

from cvars import ConVar
from events import Event
from filters.weapons import WeaponClassIter

from gungame.core.players.dictionary import player_dictionary
from gungame.core.weapons.manager import weapon_order_manager

from.info import info


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_knife_weapons = set([weapon.basename for weapon in WeaponClassIter('knife')])
_nade_weapons = set([
    weapon.basename for weapon in WeaponClassIter('explosive')])
with suppress(KeyError):
    _nade_weapons.update(set([
        weapon.basename for weapon in WeaponClassIter('incendiary')]))


# =============================================================================
# GAME EVENTS
# =============================================================================
@Event('bomb_defused')
def bomb_defused(game_event):
    """"""
    player = player_dictionary[game_event.get_int('userid')]
    levels = get_levels_to_increase(player, 'defused')
    if levels:
        player.increase_level(levels, 'bomb_defused')


@Event('bomb_exploded')
def bomb_exploded(game_event):
    """"""
    player = player_dictionary[game_event.get_int('userid')]
    levels = get_levels_to_increase(player, 'detonated')
    if levels:
        player.increase_level(levels, reason='bomb_detonated')


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def get_levels_to_increase(player, reason):
    """"""
    if reason == 'defused':
        base_levels = defused_levels.get_int()
        skip_nade = defused_skip_nade.get_int()
        skip_knife = defused_skip_knife.get_int()
    elif reason == 'detonated':
        base_levels = detonated_levels.get_int()
        skip_nade = detonated_skip_nade.get_int()
        skip_knife = detonated_skip_knife.get_int()
    else:
        raise ValueError('Invalid reason given "{0}".'format(reason))

    if base_levels <= 0:
        return 0

    for level_increase in range(base_levels + 1):
        level = player.level + level_increase
        if level > weapon_order_manager.max_levels:
            return level
        weapon = weapon_order_manager.active[level].weapon
        if (weapon in _nade_weapons and not skip_nade) or (
                weapon in _knife_weapons and not skip_knife):
            player.chat_message('BombingObjective_NoSkip_{0}'.format(
                    reason.title()), weapon=weapon)
            return level_increase
    return level_increase
