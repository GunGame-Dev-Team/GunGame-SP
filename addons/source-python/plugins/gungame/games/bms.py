# ../gungame/games/bms.py

"""BMS changes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from entities.entity import Entity
from events.custom import CustomEvent
from events.variable import ShortVariable, StringVariable
from events.resource import ResourceFile
from listeners import OnEntitySpawned
from players.entity import Player


# =============================================================================
# >> CUSTOM EVENTS
# =============================================================================
class Weapon_Fire(CustomEvent):
    userid = ShortVariable('The userid of the player that fired the weapon.')
    weapon = StringVariable('The type of weapon that was fired.')

resource_file = ResourceFile('gungame_bms', Weapon_Fire)
resource_file.write()
resource_file.load_events()


# =============================================================================
# >> LISTENERS
# =============================================================================
@OnEntitySpawned
def entity_spawned(base_entity):
    try:
        entity = Entity(base_entity.index)
    # TODO: clarify this exception
    except Exception:
        return

    if entity.classname != 'grenade_frag':
        return

    try:
        player = Player(entity.owner.index)
    # TODO: clarify this exception
    except Exception:
        return

    with Weapon_Fire() as event:
        event.userid = player.userid
        event.weapon = 'frag'
