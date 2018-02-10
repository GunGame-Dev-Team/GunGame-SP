# ../gungame/core/warmup/listeners.py

"""Listener functions for warmup."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from commands.client import client_command_manager
from entities.constants import INVALID_ENTITY_INTHANDLE
from entities.entity import Entity
from entities.helpers import index_from_inthandle
from events.manager import event_manager
from filters.players import PlayerIter
from listeners.tick import Delay
from players.entity import Player
from players.helpers import userid_from_index
from weapons.manager import weapon_manager

# GunGame
from ..status import GunGameMatchStatus
from ..teams import team_names
from ..weapons.groups import individual_weapons
from ..weapons.helpers import remove_idle_weapons


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    """Register all warmup listeners."""
    event_manager.register_for_event('player_death', _player_death)
    event_manager.register_for_event('weapon_fire', _weapon_fire)
    event_manager.register_for_event('player_spawn', _player_spawn)
    client_command_manager.register_commands('joinclass', _join_class)
    for player in PlayerIter('alive'):
        _give_warmup_weapon(player)


def unload():
    """Unregister all warmup listeners."""
    event_manager.unregister_for_event('player_death', _player_death)
    event_manager.unregister_for_event('weapon_fire', _weapon_fire)
    event_manager.unregister_for_event('player_spawn', _player_spawn)
    client_command_manager.unregister_commands('joinclass', _join_class)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def _player_death(game_event):
    # Dead Strip
    remove_idle_weapons(status=GunGameMatchStatus.WARMUP)

    # Dissolver
    victim = game_event['userid']
    try:
        inthandle = Player.from_userid(victim).ragdoll
    except ValueError:
        return
    if inthandle == INVALID_ENTITY_INTHANDLE:
        return
    entity = Entity(index_from_inthandle(inthandle))
    entity.target_name = f'ragdoll_{victim}'
    dissolver_entity = Entity.find_or_create('env_entity_dissolver')
    dissolver_entity.magnitude = 2
    dissolver_entity.dissolve_type = 0
    dissolver_entity.dissolve(f'ragdoll_{victim}')

    # DeathMatch
    Delay(
        delay=2,
        callback=_respawn_player,
        args=(victim,),
        cancel_on_level_end=True,
    )


def _weapon_fire(game_event):
    # Multi-Nade
    weapon = weapon_manager[game_event['weapon']].basename
    if weapon not in individual_weapons:
        return
    Delay(
        delay=1,
        callback=_give_weapon,
        args=(game_event['userid'], weapon),
        cancel_on_level_end=True,
    )


def _player_spawn(game_event):
    player = _get_player(game_event['userid'])
    if player is None:
        return
    if player.team_index not in team_names:
        return
    _give_warmup_weapon(player)


# =============================================================================
# >> LISTENERS
# =============================================================================
def _join_class(command, index):
    Delay(
        delay=2,
        callback=_respawn_player,
        args=(userid_from_index(index),),
        cancel_on_level_end=True,
    )


# =============================================================================
# >> HELPER FUNCTIONS
# =============================================================================
def _respawn_player(userid):
    player = _get_player(userid)
    if player is None:
        return
    player.spawn()


def _give_weapon(userid, weapon):
    player = _get_player(userid)
    if player is None:
        return
    if player.dead:
        return
    player.give_named_item(weapon_manager[weapon].name)


def _get_player(userid):
    try:
        return Player.from_userid(userid)
    except ValueError:
        return None


def _give_warmup_weapon(player):
    from .manager import warmup_manager
    _strip_player(player)
    player.give_named_item(weapon_manager[warmup_manager.weapon].name)


def _strip_player(player):
    not_filters = {'melee', 'objective', 'tool', 'grenade'}
    for weapon in player.weapons():
        tags = weapon_manager[weapon.classname].tags
        if not_filters.intersection(tags):
            continue
        weapon.remove()
