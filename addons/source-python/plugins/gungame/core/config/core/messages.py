# ../gungame/core/config/core/messages.py

"""GunGame messages configuration."""

from gungame.core.config.manager import GunGameConfigManager
from gungame.core.messages import message_manager

with GunGameConfigManager('message_settings') as config:
    leader_message = config.cvar(
            'gg_leader_messages', 1,
            description=message_manager['gg_leader_messages'])
