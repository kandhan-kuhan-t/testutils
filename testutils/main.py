from typing import Dict, Any, List
import random
import unittest.mock


class DataStore:
    def __init__(self, str_length=5):
        self._vars: Dict = {
            'int': {},
            'str': {},
            'bool': {},
            'bytes': {},
            'float': {},
            'magicmock': {},
        }
        self._str_length = str_length
        self._alphabets_small = [chr(i) for i in range(97, 97 + 26)]
        self._alphabets_large = [chr(i) for i in range(65, 65 + 26)]
        self._numbers_string = [str(i) for i in range(10)]
        self.special_characters = []
        self._characters = [
            *self._alphabets_large, *self._alphabets_small, *self._numbers_string, *self.special_characters
        ]
        self._int_min = 0
        self._int_max = 99999
        self._supported_prefixes = ['str_', 'int_', 'bool_', 'magicmock_']

    @staticmethod
    def _make_string(iterable: List[str], join_by=''):
        return join_by.join(iterable)

    def _get_random_str(self) -> str:
        string = self._make_string(random.choices(population=self._characters, k=self._str_length))
        return string

    def _get_random_int(self) -> int:
        integer = random.randint(a=self._int_min, b=self._int_max)
        return integer

    @staticmethod
    def _get_random_bool():
        boolean = random.choice([True, False])
        return boolean

    def _generate_random(self, _type: str):
        if _type in ["str", "int", "bool"]:
            return self.__getattribute__(f"_get_random_{_type}")()
        elif _type in ["magicmock"]:
            return self._generate_magic_mock()

    @staticmethod
    def _generate_magic_mock(*args, **kwargs):
        return unittest.mock.MagicMock(*args, **kwargs)

    def _get_dict_for_type(self, _type: str) -> Dict:
        return {
            "int": self._vars["int"],
            "str": self._vars["str"],
            "bool": self._vars["bool"],
            "bytes": self._vars["bytes"],
            "float": self._vars["float"],
            "magicmock": self._vars["magicmock"]
        }[_type]

    def _store_variable(self, key: str, value: Any, _type: str):
        dict_to_store: Dict = self._get_dict_for_type(_type)
        dict_to_store[key] = value

    def _get_variable(self, key: str, _type: str):
        return self._get_dict_for_type(_type)[key]

    def _is_key_stored(self, key: str, _type: str) -> bool:
        dict_to_check: Dict = self._get_dict_for_type(_type)
        return key in dict_to_check

    def _get_or_create_variable(self, key: str, _type: str):
        if self._is_key_stored(key=key, _type=_type):
            return self._get_variable(key=key, _type=_type)
        else:
            random_value = self._generate_random(_type)
            self._store_variable(key=key, value=random_value, _type=_type)
            return random_value

    def __getattr__(self, item):
        """
        If the attribute starts with a type followed by _, over-ride __getattribute__
        eg: str_name, int_age
        Otherwise, call super
        :param item:
        :return:
        """
        if not any([item.startswith(prefix) for prefix in self._supported_prefixes]):
            return super().__getattribute__(item)

        _type = item.split('_')[0]

        return self._get_or_create_variable(key=item, _type=_type)

    @property
    def str(self):
        return self._generate_random('str')

    @property
    def int(self):
        return self._generate_random('int')

    @property
    def bool(self):
        return self._generate_random('bool')

    @property
    def magicmock(self) -> unittest.mock.MagicMock:
        return self._generate_magic_mock()
