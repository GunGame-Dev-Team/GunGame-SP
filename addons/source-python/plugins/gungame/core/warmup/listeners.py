# ../gungame/core/warmup/listeners.py

""""""

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
from filters.weapons import WeaponIter
from listeners.tick import Delay
from players.entity import Player
from players.helpers import userid_from_index
from weapons.manager import weapon_manager

# GunGame
from ..teams import team_names
from ..weapons.groups import all_grenade_weapons


# =============================================================================
# >> LOAD & UNLOAD
# =============================================================================
def load():
    event_manager.register_for_event('player_death', _player_death)
    event_manager.register_for_event('weapon_fire', _weapon_fire)
    event_manager.register_for_event('player_spawn', _player_spawn)
    client_command_manager.register_commands('joinclass', _join_class)
    for player in PlayerIter('alive'):
        _give_warmup_weapon(player)


def unload():
    event_manager.unregister_for_event('player_death', _player_death)
    event_manager.unregister_for_event('weapon_fire', _weapon_fire)
    event_manager.unregister_for_event('player_spawn', _player_spawn)
    client_command_manager.unregister_commands('joinclass', _join_class)


# =============================================================================
# >> GAME EVENTS
# =============================================================================
def _player_death(game_event):
    # Dead Strip
    for weapon in WeaponIter(
        not_filters=(
            tag for tag in ('tool', 'objective') if tag in weapon_manager.tags
        )
    ):
        if weapon.owner is None:
            weapon.remove()

    # Dissolver
    victim = game_event['userid']
    try:
        inthandle = Player.from_userid(victim).ragdoll
    except ValueError:
        return
    if inthandle == INVALID_ENTITY_INTHANDLE:
        return
    entity = Entity(index_from_inthandle(inthandle))
    entity.target_name = 'ragdoll_{userid}'.format(userid=victim)
    dissolver_entity = Entity.find_or_create('env_entity_dissolver')
    dissolver_entity.magnitude = 2
    dissolver_entity.dissolve_type = 0
    dissolver_entity.dissolve('ragdoll_{userid}'.format(userid=victim))

    # DeathMatch
    Delay(2, _respawn_player, (victim, ))


def _weapon_fire(game_event):
    # Multi-Nade
    weapon = game_event['weapon']
    if weapon not in all_grenade_weapons:
        return
    Delay(1, _give_weapon, (game_event['userid'], weapon))


def _player_spawn(game_event):
    player = _get_player(game_event['userid'])
    if player is None:
        return
    if player.team not in team_names:
        return
    _give_warmup_weapon(player)


# =============================================================================
# >> LISTENERS
# =============================================================================
def _join_class(command, index):
    Delay(2, _respawn_player, (userid_from_index(index), ))


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
