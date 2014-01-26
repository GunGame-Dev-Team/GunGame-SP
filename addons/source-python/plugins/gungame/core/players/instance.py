# ../gungame/core/players/instance.py

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python Imports
#   Players
from players.helpers import index_from_userid
from players.helpers import uniqueid_from_playerinfo


# =============================================================================
# >> CLASSES
# =============================================================================
class _GunGamePlayer(PlayerEntity):
    '''Class used to interact directly with a specific player'''

    def __new__(cls, userid):
        '''Stores the userid and uniqueid on instantiation'''
        index = index_from_userid(userid)
        if not index:
            raise ValueError('Invalid userid "%s"' % userid)
        super(_GunGamePlayer, cls).__new__(cls, index)
