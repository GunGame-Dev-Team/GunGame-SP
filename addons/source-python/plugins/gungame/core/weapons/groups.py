from filters.weapons import WeaponClassIter


__all__ = (
    'all_weapons',
    'explosive_weapons',
    'grenade_weapons',
    'incendiary_weapons',
    'melee_weapons',
    'other_weapons',
    'primary_weapons',
    'secondary_weapons',
)

primary_weapons = set(
    weapon.basename for weapon in WeaponClassIter(
        is_filters='primary',
    )
)
secondary_weapons = set(
    weapon.basename for weapon in WeaponClassIter(
        is_filters='secondary',
    )
)
explosive_weapons = set(
    weapon.basename for weapon in WeaponClassIter(
        is_filters='explosive',
        not_filters='objective',
    )
)
incendiary_weapons = set(
    weapon.basename for weapon in WeaponClassIter(
        is_filters='incendiary',
        not_filters=['explosive', 'objective'],
    )
)
grenade_weapons = set(
    weapon.basename for weapon in WeaponClassIter(
        is_filters='grenade',
        not_filters=['explosive', 'incendiary', 'objective'],
    )
)
melee_weapons = set(
    weapon.basename for weapon in WeaponClassIter(
        is_filters='melee',
    )
)
other_weapons = set(
    weapon.basename for weapon in WeaponClassIter(
        not_filters=[
            'primary', 'secondary', 'explosive', 'incendiary',
            'grenade', 'melee', 'objective', 'tool'
        ]
    ) if len(weapon.tags) > 1
)
all_weapons = (
    primary_weapons | secondary_weapons | explosive_weapons |
    incendiary_weapons | grenade_weapons | melee_weapons | other_weapons
)
