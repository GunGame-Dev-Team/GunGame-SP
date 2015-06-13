# ../gungame/plugins/included/gg_hostage_objective/gg_hostage_objective.py

""""""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Contextlib
from contextlib import suppress

# Source.Python Imports
#   Cvars
from cvars import ConVar
#   Events
from events import Event
#   Filters
from filters.entities import EntityIter
from filters.errors import FilterError
from filters.weapons import WeaponClassIter

# GunGame Imports
#   Players
from gungame.core.players.attributes import player_attributes
from gungame.core.players.dictionary import player_dictionary
#   Weapons
from gungame.core.weapons.manager import weapon_order_manager

# Script Imports
from .info import info


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
_knife_weapons = set(WeaponClassIter('knife', return_types='basename'))
_nade_weapons = set(WeaponClassIter('explosive', return_types='basename'))
with suppress(FilterError):
    _nade_weapons.update(set(
        WeaponClassIter('incendiary', return_types='basename')))

_hostage_entities = EntityIter('hostage_entity', return_types='entity')


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    """"""
    player_attributes.register_attribute('hostage_rescues', 0)
    player_attributes.register_attribute('hostage_stops', 0)
    player_attributes.register_attribute('hostage_kills', 0)


def unload():
    """"""
    player_attributes.unregister_attribute('hostage_rescues')
    player_attributes.unregister_attribute('hostage_stops')
    player_attributes.unregister_attribute('hostage_kills')


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event
def hostage_rescue(game_event):
    """"""
    player = player_dictionary[game_event.get_int('userid')]
    player.hostage_rescues += 1
    if player.hostage_rescues < ConVar(
            'gg_hostage_objective_rescued_count').get_int():
        return
    player.hostage_rescues = 0
    levels = get_levels_to_increase(player, 'rescued')
    if levels:
        player.increase_level(levels, reason='hostage_rescued')


@Event
def player_death(game_event):
    """"""
    victim = player_dictionary[game_event.get_int('userid')]
    hostages = len(filter(
        lambda entity: entity.leader == victim.inthandle, _hostage_entities))
    if not hostages:
        return
    attacker = game_event.get_int('attacker')
    if not attacker:
        return
    player = player_dictionary[attacker]
    if player.team == victim.team:
        return
    player.hostage_stops += hostages
    required = ConVar('gg_hostage_objective_stopped_count').get_int()
    if player.hostage_stops < required:
        return
    player.hostage_stops -= required
    levels = get_levels_to_increase(player, 'stopped')
    if levels:
        player.increase_level(levels, reason='hostage_stopped')


@Event
def hostage_killed(game_event):
    """"""
    attacker = game_event.get_int('attacker')
    if not attacker:
        return
    player = player_dictionary[attacker]
    player.hostage_kills += 1
    if player.hostage_kills < ConVar(
            'gg_hostage_objective_killed_count').get_int():
        return
    player.hostage_kills = 0
    player.decrease_level(ConVar(
        'gg_hostage_objective_killed_levels').get_int(),
        reason='hostage_killed')
    player.chat_message(
        message='HostageObjective_LevelDown_Killed', newlevel=player.level)


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def get_levels_to_increase(player, reason):
    """"""
    base_levels = ConVar(
        'gg_hostage_objective_{0}_levels'.format(reason)).get_int()
    if base_levels <= 0:
        return 0
    skip_nade = ConVar(
        'gg_hostage_objective_{0}_skip_nade'.format(reason)).get_int()
    skip_knife = ConVar(
        'gg_hostage_objective_{0}_skip_knife'.format(reason)).get_int()

    for level_increase in range(base_levels + 1):
        level = player.level + level_increase
        if level > weapon_order_manager.max_levels:
            return level
        weapon = weapon_order_manager.active[level].weapon
        if (weapon in _nade_weapons and not skip_nade) or (
                weapon in _knife_weapons and not skip_knife):
            player.chat_message(message='HostageObjective_NoSkip_{0}'.format(
                reason.title()), level=weapon)
            return level_increase
    return level_increase
