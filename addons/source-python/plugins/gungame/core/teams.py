# ../gungame/core/teams.py

"""Provides team data."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from filters.entities import EntityIter
from players.teams import team_managers, teams_by_number


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'team_levels',
    'team_names',
)


# =============================================================================
# >> CLASSES
# =============================================================================
class _TeamLevels(dict):
    def clear(self):
        for x in self:
            self[x] = 0


class _TeamNames(dict):
    def __missing__(self, key):
        if teams_by_number.get(key, 'un') in ('un', 'spec'):
            raise ValueError(
                'Invalid team number "{key}".'.format(
                    key=key,
                )
            )

        value = None
        for _class_name in team_managers:
            for _entity in EntityIter(_class_name):
                if _entity.team == key:
                    value = self[key] = _entity.team_name
                    team_levels[key] = 0
                    break
            if value is not None:
                break
        else:
            raise LookupError(
                'Entity not found for team "{key}".'.format(
                    key=key,
                )
            )


# =============================================================================
# >> GLOBAL VARIABLES
# =============================================================================
team_names = _TeamNames()
team_levels = _TeamLevels()
