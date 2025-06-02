# ../gungame/plugins/included/gg_bombing_objective/gg_bombing_objective.py

"""Plugin that adds leveling based on bombing objectives."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events import Event

# GunGame
from gungame.core.players.dictionary import player_dictionary
from gungame.core.status import (
    GunGameMatchStatus,
    GunGameRoundStatus,
    GunGameStatus,
)
from gungame.core.weapons.groups import all_grenade_weapons, melee_weapons
from gungame.core.weapons.manager import weapon_order_manager

# Plugin
from .configuration import (
    defused_levels,
    defused_skip_knife,
    defused_skip_nade,
    detonated_levels,
    detonated_skip_knife,
    detonated_skip_nade,
)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event("bomb_defused", "bomb_exploded")
def _bomb_event(game_event):
    """Level the defuser/detonator up."""
    if (
        GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE or
        GunGameStatus.ROUND is GunGameRoundStatus.INACTIVE
    ):
        return

    event_name = game_event.name
    player = player_dictionary[game_event["userid"]]
    if player is None:
        return

    levels = _get_levels_to_increase(player, event_name)
    if not levels:
        return

    player.increase_level(
        levels=levels,
        reason=event_name,
    )
    player.chat_message(
        message=f"BombingObjective:Leveled:{event_name}",
        levels=levels,
    )


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _get_levels_to_increase(player, event_name):
    """Return the number of levels to increase the player."""
    if event_name == "bomb_defused":
        base_levels = int(defused_levels)
        skip_nade = int(defused_skip_nade)
        skip_knife = int(defused_skip_knife)
    elif event_name == "bomb_exploded":
        base_levels = int(detonated_levels)
        skip_nade = int(detonated_skip_nade)
        skip_knife = int(detonated_skip_knife)
    else:
        msg = f'Invalid reason given "{event_name}".'
        raise ValueError(msg)

    if base_levels <= 0:
        return 0

    level_increase = 0

    for level_increase in range(1, base_levels + 1):
        level = player.level + level_increase
        if level > weapon_order_manager.max_levels:
            return level_increase
        skip_weapon = weapon_order_manager.active[level - 1].weapon
        if (
            (skip_weapon in all_grenade_weapons and not skip_nade) or
            (skip_weapon in melee_weapons and not skip_knife)
        ):
            player.chat_message(
                f"BombingObjective:NoSkip:{event_name}",
                weapon=skip_weapon,
            )
            return level_increase - 1
    return level_increase
