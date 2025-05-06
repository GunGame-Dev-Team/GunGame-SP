# ../gungame/plugins/included/gg_multi_level/sounds.py

"""Register multi-leveling sounds."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# GunGame
from gungame.core.sounds.manager import sound_manager

# =============================================================================
# >> SOUND REGISTRATION
# =============================================================================
sound_manager.register_sound(
    sound_name="multi_level",
    default="source-python/gungame/default/smb_star.mp3",
)
