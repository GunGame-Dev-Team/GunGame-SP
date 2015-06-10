# ../gungame/core/config/core/messages.py

"""GunGame messages configuration."""

from gungame.core.config.manager import GunGameConfigManager
from gungame.core.messages import message_manager

with GunGameConfigManager('message_settings') as config:
    leader_messages = config.cvar(
        'gg_leader_messages', 1,
        description=message_manager['gg_leader_messages'])

    level_info = config.cvar(
        'gg_level_info', 1, description=message_manager['gg_level_info'])

    winner_messages = config.cvar(
        'gg_winner_messages', 1,
        description=message_manager['gg_winner_messages'])
