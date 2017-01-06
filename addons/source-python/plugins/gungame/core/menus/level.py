# ../gungame/core/menus/level.py

"""Level menu functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from menus import SimpleMenu, SimpleOption, Text
from players.helpers import userid_from_index

# GunGame
from . import menu_strings
from ..commands.registration import register_command_callback
from ..leaders import leader_manager
from ..players.dictionary import player_dictionary
from ..plugins.manager import gg_plugin_manager
from ..status import GunGameMatchStatus, GunGameStatus
from ..teams import team_levels, team_names


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'send_level_menu',
)


# =============================================================================
# >> FUNCTIONS
# =============================================================================
@register_command_callback('level', 'Level:Text')
def send_level_menu(index):
    """Send the level menu to the player."""
    menu = SimpleMenu()
    player = player_dictionary[userid_from_index(index)]
    menu.append(
        SimpleOption(
            1,
            menu_strings['Level:Title'],
            selectable=False,
        )
    )
    language = player.language
    if GunGameStatus.MATCH is not GunGameMatchStatus.ACTIVE:
        menu.append(menu_strings['Inactive'])
    elif gg_plugin_manager.is_team_game:
        if player.team not in team_levels:
            menu.append(Text(menu_strings['Level:Inactive']))
        else:
            team_level = team_levels[player.team]
            leader_level = max(team_levels.values())
            teams = [
                team_names[num] for num, level in team_levels.items()
                if level == leader_level
            ]
            menu.append(
                menu_strings['Level:Team'].get_string(
                    language=language,
                    level=team_level,
                )
            )
            if team_level < leader_level:
                menu.append(
                    menu_strings['Level:Team:Trailing'].get_string(
                        language=language,
                        levels=leader_level - team_level,
                    )
                )
            elif len(teams) == 1:
                second_place = max([
                    x for x in team_levels.values() if x != leader_level
                ])
                menu.append(
                    menu_strings['Level:Team:Leading'].get_string(
                        language=language,
                        levels=leader_level - second_place
                    )
                )
            elif len(teams) == len(team_levels):
                if len(teams) == 2:
                    menu.append(menu_strings['Level:Team:Tied'])
                else:
                    menu.append(menu_strings['Level:Team:All'])
            else:
                message = menu_strings['Level:Team:Multiple'].get_string(
                    language=language,
                )
                message += '\n\t* {teams}'.format(
                    teams=', '.join(teams)
                )
                menu.append(message)
    elif player.team < 2:
        menu.append(Text(menu_strings['Level:Inactive']))
    else:
        menu.append(
            Text(
                menu_strings['Level:Current'].get_string(
                    language,
                    level=player.level,
                )
            )
        )
        menu.append(
            Text(
                menu_strings['Level:Weapon'].get_string(
                    language,
                    kills=player.level_multi_kill - player.multi_kill,
                    weapon=player.level_weapon,
                )
            )
        )
        leaders = leader_manager.current_leaders
        if leaders is None:
            menu.append(Text(menu_strings['Leader:None']))
        elif player.userid not in leaders:
            menu.append(
                Text(
                    menu_strings['Level:Trailing'].get_string(
                        language,
                        levels=leader_manager.leader_level - player.level,
                    )
                )
            )
        elif len(leaders) > 1:
            menu.append(Text(menu_strings['Level:Tied']))
        else:
            menu.append(Text(menu_strings['Level:Leading']))
        menu.append(
            SimpleOption(
                2,
                menu_strings['Level:Wins-Title'],
                selectable=False,
            )
        )
        menu.append(
            Text(
                menu_strings['Level:Wins'].get_string(
                    language,
                    wins=player.wins,
                )
            )
        )
    menu.send(index)
