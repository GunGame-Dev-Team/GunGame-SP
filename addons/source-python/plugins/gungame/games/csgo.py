from gungame.core.players.weapons import _PlayerWeapons
from gungame.core.messages import message_manager


def _give_named_item(player, weapon):
    """"""
    player.give_named_item(weapon, 0, None, True)

_PlayerWeapons._give_named_item = _give_named_item


def _no_message(*args, **kwargs):
    ...

message_manager.center_message = _no_message
message_manager.echo_message = _no_message
message_manager.hud_message = _no_message
