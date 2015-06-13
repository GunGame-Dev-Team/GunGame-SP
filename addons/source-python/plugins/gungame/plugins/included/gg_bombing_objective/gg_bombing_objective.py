# ../gungame/plugins/included/gg_bombing_objective/gg_bombing_objective.py

""""""

# =============================================================================
# >> IMPORTS
# =============================================================================
from contextlib import suppress

from cvars import ConVar
from events import Event
from filters.errors import FilterError
from filters.weapons import WeaponClassIter

from gungame.core.players.dictionary import player_dictionary
from gungame.core.weapons.manager import weapon_order_manager

from.info import info


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_knife_weapons = set(WeaponClassIter('knife', return_types='basename'))
_nade_weapons = set(WeaponClassIter('explosive', return_types='basename'))
with suppress(FilterError):
    _nade_weapons.update(set(
        WeaponClassIter('incendiary', return_types='basename')))


# =============================================================================
# GAME EVENTS
# =============================================================================
@Event
def bomb_defused(game_event):
    """"""
    player = player_dictionary[game_event.get_int('userid')]
    levels = get_levels_to_increase(player, 'defused')
    if levels:
        player.increase_level(levels, 'bomb_defused')


@Event
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
    base_levels = ConVar(
        'gg_bombing_objective_{0}_levels'.format(reason)).get_int()
    if base_levels <= 0:
        return 0
    skip_nade = ConVar(
        'gg_bombing_objective_{0}_skip_nade'.format(reason)).get_int()
    skip_knife = ConVar(
        'gg_bombing_objective_{0}_skip_knife'.format(reason)).get_int()

    for level_increase in range(base_levels + 1):
        level = player.level + level_increase
        if level > weapon_order_manager.max_levels:
            return level
        weapon = weapon_order_manager.active[level].weapon
        if (weapon in _nade_weapons and not skip_nade) or (
                weapon in _knife_weapons and not skip_knife):
            player.chat_message(
                message='BombingObjective_NoSkip_{0}'.format(
                    reason.title()), level=weapon))
            return level_increase
    return level_increase
