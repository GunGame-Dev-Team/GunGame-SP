# ../gungame/core/menus/level.py

"""Level menu functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from menus import SimpleMenu, SimpleOption, Text
from players.helpers import userid_from_index

# GunGame
from ..leaders import leader_manager
from . import _menu_strings
from ..players.dictionary import player_dictionary
from ..plugins.manager import gg_plugin_manager
from ..status import GunGameMatchStatus, GunGameStatus


# =============================================================================
# >> FUNCTIONS
# =============================================================================
def send_level_menu(index):
    """Send the level menu to the player."""
    menu = SimpleMenu()
    player = player_dictionary[userid_from_index(index)]
    menu.append(
        SimpleOption(
            1,
            _menu_strings['Level:Title'],
            selectable=False,
        )
    )
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        menu.append(_menu_strings['Inactive'])
    elif 'gg_teamplay' in gg_plugin_manager:
        # TODO: Implement teamplay menus once teamplay is implemented
        menu.clear()
        menu.append(_menu_strings['Level:TeamPlay'])
    elif player.team < 2:
        menu.append(Text(_menu_strings['Level:Inactive']))
    else:
        menu.append(
            Text(
                _menu_strings['Level:Current'].get_string(
                    player.language,
                    level=player.level,
                )
            )
        )
        menu.append(
            Text(
                _menu_strings['Level:Weapon'].get_string(
                    player.language,
                    kills=player.level_multi_kill - player.multi_kill,
                    weapon=player.level_weapon,
                )
            )
        )
        leaders = leader_manager.current_leaders
        if leaders is None:
            menu.append(Text(_menu_strings['Leader:None']))
        elif player.userid not in leaders:
            menu.append(
                Text(
                    _menu_strings['Level:Trailing'].get_string(
                        player.language,
                        levels=leader_manager.leader_level - player.level,
                    )
                )
            )
        elif len(leaders) > 1:
            menu.append(Text(_menu_strings['Level:Tied']))
        else:
            menu.append(Text(_menu_strings['Level:Leading']))
        menu.append(
            SimpleOption(
                2,
                _menu_strings['Level:Wins-Title'],
                selectable=False,
            )
        )
        menu.append(
            Text(
                _menu_strings['Level:Wins'].get_string(
                    player.language,
                    wins=player.wins,
                )
            )
        )
    menu.send(index)
