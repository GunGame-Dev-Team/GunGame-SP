# ../gungame/plugins/included/gg_hostage_objective/gg_hostage_objective.py

"""Plugin that adds leveling based on hostage objectives."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events import Event
from filters.entities import EntityIter

# GunGame
from gungame.core.players.attributes import player_attributes
from gungame.core.players.dictionary import player_dictionary
from gungame.core.weapons.groups import all_grenade_weapons, melee_weapons
from gungame.core.weapons.manager import weapon_order_manager

# Plugin
from .configuration import (
    killed_count, killed_levels, rescued_count, rescued_levels,
    rescued_skip_knife, rescued_skip_nade, stopped_count, stopped_levels,
    stopped_skip_knife, stopped_skip_nade,
)


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    """Add the player hostage attributes."""
    player_attributes.register_attribute('hostage_rescues', 0)
    player_attributes.register_attribute('hostage_stops', 0)
    player_attributes.register_attribute('hostage_kills', 0)


def unload():
    """Remove the player hostage attributes."""
    player_attributes.unregister_attribute('hostage_rescues')
    player_attributes.unregister_attribute('hostage_stops')
    player_attributes.unregister_attribute('hostage_kills')


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('hostage_rescued')
def _hostage_rescued(game_event):
    """Level the rescuer up."""
    player = player_dictionary[game_event['userid']]
    player.hostage_rescues += 1
    required = rescued_count.get_int()
    if player.hostage_rescues < required:
        return
    player.hostage_rescues = 0
    levels = _get_levels_to_increase(player, 'rescued')
    if not levels:
        return
    player.increase_level(
        levels=levels,
        reason='hostage_rescued',
    )
    player.chat_message(
        message='HostageObjective:Leveled:Rescued',
        levels=levels,
        count=required,
    )


@Event('player_death')
def _player_death(game_event):
    """Level the stopper up."""
    victim = player_dictionary[game_event['userid']]
    hostages = len([
        entity for entity in EntityIter('hostage_entity')
        if entity.leader == victim.inthandle
    ])
    if not hostages:
        return
    attacker = game_event['attacker']
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
    levels = _get_levels_to_increase(player, 'stopped')
    if not levels:
        return
    player.increase_level(
        levels=levels,
        reason='hostage_stopped',
    )
    player.chat_message(
        message='HostageObjective:Leveled:Stopped',
        levels=levels,
        count=required,
    )


@Event('hostage_killed')
def _hostage_killed(game_event):
    """Level the killer down."""
    levels = killed_levels.get_int()
    min_count = killed_count.get_int()
    if levels < 1 or min_count < 1:
        return
    attacker = game_event['attacker']
    if not attacker:
        return
    player = player_dictionary[attacker]
    player.hostage_kills += 1
    if player.hostage_kills < min_count:
        return
    player.hostage_kills = 0
    starting_level = player.level
    player.decrease_level(
        levels=levels,
        reason='hostage_killed',
    )
    if player.level < starting_level:
        player.chat_message(
            message='HostageObjective:Leveled:Killed',
            player=player,
            count=min_count,
        )


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _get_levels_to_increase(player, reason):
    """Return the number of levels to increase the player."""
    if reason == 'rescued':
        base_levels = rescued_levels.get_int()
        skip_nade = rescued_skip_nade.get_int()
        skip_knife = rescued_skip_knife.get_int()
    elif reason == 'stopped':
        base_levels = stopped_levels.get_int()
        skip_nade = stopped_skip_nade.get_int()
        skip_knife = stopped_skip_knife.get_int()
    else:
        raise ValueError(
            'Invalid reason given "{reason}".'.format(reason=reason)
        )

    if base_levels <= 0:
        return 0

    level_increase = 0

    for level_increase in range(base_levels + 1):
        level = player.level + level_increase
        if level > weapon_order_manager.max_levels:
            return level_increase
        weapon = weapon_order_manager.active[level].weapon
        if (
            (weapon in all_grenade_weapons and not skip_nade) or
            (weapon in melee_weapons and not skip_knife)
        ):
            player.chat_message(
                'HostageObjective:NoSkip:{reason}'.format(
                    reason=reason.title()
                ),
                weapon=weapon,
            )
            return level_increase
    return level_increase
