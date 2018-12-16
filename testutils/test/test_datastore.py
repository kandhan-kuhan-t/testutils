from unittest import TestCase
from testutils import DataStore
from unittest import mock


class TestDataStore(TestCase):
    def setUp(self):
        self.ds = DataStore()

    def test_get_random_str_type(self):
        self.assertIsInstance(self.ds._get_random_str(), str)

    def test_get_random_str_length(self):
        self.ds._str_length = 10
        self.assertEqual(len(self.ds._get_random_str()), 10)

    def test_get_random_str_uniqueness(self):
        random_string = self.ds._get_random_str()
        other_random_strings = [self.ds._get_random_str() for _ in range(1000)]
        self.assertNotIn(random_string, other_random_strings)

    def test_get_random_int_type(self):
        self.assertIsInstance(self.ds._get_random_int(), int)

    def test_get_random_int_boundary(self):
        self.ds._int_min = 0
        self.ds._int_max = 1000
        random_ints = [self.ds._get_random_int() for _ in range(1000)]
        for random_int in random_ints:
            self.assertGreaterEqual(random_int, 0)
            self.assertLessEqual(random_int, 1000)

    def test_get_dict_for_type(self):
        _types = ['str', 'int', 'bytes', 'float', 'bool']
        _invalid_types = ['some_type', 'someother_type']

        for _type in _types:
            with self.subTest(_type=_type):
                return_value = self.ds._get_dict_for_type(_type=_type)
                self.assertIsInstance(return_value, dict)

        for _type in _invalid_types:
            with self.subTest(_type=_type):
                self.assertRaises(KeyError, self.ds._get_dict_for_type, _type=_type)

    @mock.patch.object(DataStore, '_get_dict_for_type')
    def test_store_variable(self, mockmethod):
        store_dict = {}
        mockmethod.return_value = store_dict

        self.assertIsNone(store_dict.get("key"))
        self.ds._store_variable(key='key', value='value', _type='str')
        self.assertIsNotNone(store_dict.get("key"))

        self.assertEqual(store_dict["key"], 'value')

    @mock.patch.object(DataStore, '_get_dict_for_type')
    def test_is_key_stored(self, mockmethod):
        store_dict = {}
        mockmethod.return_value = store_dict

        self.assertFalse(self.ds._is_key_stored(key="key", _type="str"))

        store_dict["key"] = "value"

        self.assertTrue(self.ds._is_key_stored(key="key", _type="str"))

    def test_generate_magicmock(self):
        self.assertIsInstance(self.ds._generate_magic_mock(), mock.MagicMock)
        self.assertIs(self.ds.magicmock_magic, self.ds.magicmock_magic)
        self.assertIsNot(self.ds.magicmock, self.ds.magicmock)
