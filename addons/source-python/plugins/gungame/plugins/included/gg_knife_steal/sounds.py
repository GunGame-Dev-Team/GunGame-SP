# ../gungame/plugins/included/gg_knife_steal/sounds.py

"""Register knife steal sounds."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.sounds.manager import sound_manager


# =============================================================================
# >> SOUND REGISTRATION
# =============================================================================
sound_manager.register_sound(
    sound_name='knife_steal',
    default='source-python/gungame/default/smb3_1-up.mp3',
)
