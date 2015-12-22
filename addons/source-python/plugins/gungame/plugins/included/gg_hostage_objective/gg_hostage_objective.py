# ../gungame/plugins/included/gg_hostage_objective/gg_hostage_objective.py

""""""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Contextlib
from contextlib import suppress

# Source.Python Imports
#   Events
from events import Event
#   Filters
from filters.entities import EntityIter
from filters.weapons import WeaponClassIter

# GunGame Imports
#   Players
from gungame.core.players.attributes import player_attributes
from gungame.core.players.dictionary import player_dictionary
#   Weapons
from gungame.core.weapons.manager import weapon_order_manager

# Script Imports
from .configuration import rescued_levels
from .configuration import rescued_count
from .configuration import rescued_skip_knife
from .configuration import rescued_skip_nade
from .configuration import stopped_levels
from .configuration import stopped_count
from .configuration import stopped_skip_knife
from .configuration import stopped_skip_nade
from .configuration import killed_levels
from .configuration import killed_count


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
@Event('hostage_rescued')
def hostage_rescued(game_event):
    """"""
    player = player_dictionary[game_event.get_int('userid')]
    player.hostage_rescues += 1
    if player.hostage_rescues < rescued_count.get_int():
        return
    player.hostage_rescues = 0
    levels = get_levels_to_increase(player, 'rescued')
    if levels:
        player.increase_level(levels, reason='hostage_rescued')


@Event('player_death')
def player_death(game_event):
    """"""
    victim = player_dictionary[game_event.get_int('userid')]
    hostages = len(filter(
        lambda entity: entity.leader == victim.inthandle,
        EntityIter('hostage_entity')))
    if not hostages:
        return
    attacker = game_event.get_int('attacker')
    if not attacker:
        return
    player = player_dictionary[attacker]
    if player.team == victim.team:
        return
    player.hostage_stops += hostages
    required = stopped_count.get_int()
    if player.hostage_stops < required:
        return
    player.hostage_stops -= required
    levels = get_levels_to_increase(player, 'stopped')
    if levels:
        player.increase_level(levels, reason='hostage_stopped')


@Event('hostage_killed')
def hostage_killed(game_event):
    """"""
    attacker = game_event.get_int('attacker')
    if not attacker:
        return
    player = player_dictionary[attacker]
    player.hostage_kills += 1
    if player.hostage_kills < killed_count.get_int():
        return
    player.hostage_kills = 0
    player.decrease_level(killed_levels.get_int(), reason='hostage_killed')
    player.chat_message('HostageObjective_LevelDown_Killed', player=player)


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def get_levels_to_increase(player, reason):
    """"""
    if reason == 'rescued':
        base_levels = rescued_levels.get_int()
        skip_nade = rescued_skip_nade.get_int()
        skip_knife = rescued_skip_knife.get_int()
    elif reason == 'stopped':
        base_levels = stopped_levels.get_int()
        skip_nade = stopped_skip_nade.get_int()
        skip_knife = stopped_skip_knife.get_int()
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
            player.chat_message('HostageObjective_NoSkip_{0}'.format(
                reason.title()), weapon=weapon)
            return level_increase
    return level_increase
