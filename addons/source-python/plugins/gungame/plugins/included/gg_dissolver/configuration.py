# ../gungame/plugins/included/gg_dissolver/configuration.py

"""Creates the gg_disable_objectives configuration."""

# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from entities.constants import DissolveType

# GunGame
from gungame.core.config.manager import GunGameConfigManager

# Plugin
from .info import info


# =============================================================================
# >> ALL DECLARATION
# =============================================================================
__all__ = (
    'dissolver_delay',
    'dissolver_type',
    'magnitude',
)


# =============================================================================
# >> CONFIGURATION
# =============================================================================
with GunGameConfigManager(info.name) as _config:

    with _config.cvar(
        name='type',
    ) as dissolver_type:

        for _name in DissolveType.__members__:
            dissolver_type.Options.append(
                f'{getattr(DissolveType, _name).real} = {_name}'
            )

        _num_dissolve_types = len(DissolveType.__members__)
        dissolver_type.add_text(
            random=_num_dissolve_types,
            remove=_num_dissolve_types + 1,
        )

    with _config.cvar(
        name='magnitude',
        default=2,
    ) as magnitude:
        magnitude.add_text()

    with _config.cvar(
        name='delay',
    ) as dissolver_delay:
        dissolver_delay.add_text()
