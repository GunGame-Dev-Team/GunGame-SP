# ../gungame/games/hl2mp.py

"""HL2:DM changes."""

# =============================================================================
# >> IMPORTS
# =============================================================================
from entities.entity import Entity
from events.custom import CustomEvent
from events.resource import ResourceFile
from events.variable import ShortVariable, StringVariable
from listeners import OnEntitySpawned
from players.entity import Player


# =============================================================================
# >> CUSTOM EVENTS
# =============================================================================
# ruff: noqa: N801
class Weapon_Fire(CustomEvent):
    """Custom event to fire when players throw grenades."""

    userid = ShortVariable("The userid of the player that fired the weapon.")
    weapon = StringVariable("The type of weapon that was fired.")


resource_file = ResourceFile("gungame_hl2mp", Weapon_Fire)
resource_file.write()
resource_file.load_events()


# =============================================================================
# >> LISTENERS
# =============================================================================
@OnEntitySpawned
def _entity_spawned(base_entity):
    """Fire weapon_fire event when a grenade is thrown."""
    try:
        entity = Entity(base_entity.index)
    except ValueError:
        return

    if entity.classname != "npc_grenade_frag":
        return

    try:
        player = Player(entity.owner.index)
    except ValueError:
        return

    with Weapon_Fire() as event:
        event.userid = player.userid
        event.weapon = "frag"
