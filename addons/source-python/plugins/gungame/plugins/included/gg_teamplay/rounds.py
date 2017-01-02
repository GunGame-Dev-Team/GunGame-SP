# ../gungame/plugins/included/gg_teamplay/rounds.py

"""Round-based teamplay functionality."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from events import Event

# GunGame
from gungame.core.rules.strings import rules_translations

# Plugin
from .manager import team_dictionary
from .rules import teamplay_rules


# =============================================================================
# >> RULES
# =============================================================================
for _item in list(teamplay_rules):
    if _item.startswith('Teamplay:Deathmatch:'):
        teamplay_rules.unregister_rule(_item)

for _key, _value in rules_translations.items():
    if _key.startswith('Teamplay:Rounds:'):
        teamplay_rules.register_rule(
            name=_key,
            value=_value,
        )


# =============================================================================
# >> GAME EVENTS
# =============================================================================
@Event('round_end')
def _increment_winning_team(game_event):
    winner = team_dictionary.get(game_event['winner'])
    if winner is None:
        return

    winner.increase_multi_kill()


@Event('round_start')
def _send_level_messages(game_event):
    for team in team_dictionary:
        team.send_current_level_message()
