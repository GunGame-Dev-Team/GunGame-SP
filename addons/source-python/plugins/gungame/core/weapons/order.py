from cvars import ConVar
from filters.weapons import WeaponClassIter
from gungame.core.weapons.errors import WeaponOrderError


_primary_weapons = list(WeaponClassIter('primary', return_types='basename'))
_secondary_weapons = list(
    WeaponClassIter('secondary', return_types='basename'))
_multikill_weapons = _primary_weapons + _secondary_weapons


class WeaponOrder(dict):

    """"""

    def __init__(self, filepath):
        """"""
        super(WeaponOrder, self).__init__()
        with filepath.open() as open_file:
            level = 0
            for line in open_file:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('//'):
                    continue
                try:
                    weapon, multikill = line.split()
                except ValueError:
                    weapon = line
                    multikill = 1
                try:
                    multikill = int(multikill)
                except ValueError:
                    raise WeaponOrderError()
                level += 1
                self[level] = _LevelWeapon(weapon, multikill)
        self._filepath = filepath
        self._name = self.filepath.namebase
        self._title = self.name.replace('_', ' ').title()
        self._random_order = None

    @property
    def name(self):
        """"""
        return self._name

    @property
    def filepath(self):
        """"""
        return self._filepath

    @property
    def title(self):
        """"""
        return self._title

    @property
    def max_levels(self):
        return len(self)

    @property
    def random_order(self):
        return self._random_order

    def randomize_order(self):
        self._random_order = dict()
        randomize_weapons = self.values()
        keep_at_end = list()
        for weapon in reversed(randomize_weapons):
            if weapon.weapon in _multikill_weapons:
                break
            keep_at_end.append(weapon)
        if keep_at_end:
            keep_at_end = reversed(keep_at_end)
            randomize_weapons = randomize_weapons[:-len(keep_at_end)]
        shuffle(randomize_weapons)
        randomize_weapons.extend(keep_at_end)
        for level, value in enumerate(values, 1):
            self._random_order[level] = value


class _LevelWeapon(object):

    """"""

    def __init__(self, weapon, multikill):
        """"""
        self._weapon = weapon
        self._multikill = multikill

    @property
    def weapon(self):
        """"""
        return self._weapon

    @property
    def multikill(self):
        """"""
        override = ConVar('gg_multikill_override').get_int()
        if self.weapon in _multikill_weapons and override:
            return override
        return self._multikill
