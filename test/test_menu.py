from unittest import TestCase
from menu import Menu


class TestMenu(TestCase):

    def setUp(self):
        self.menu = Menu()

        def a():
            pass

        def b():
            pass

        self.a = a
        self.b = b

        self.menu.add_option('a', 'aaaaa', a)
        self.menu.add_option('b', 'bbbbb', b)


    def test_add_option(self):
        self.assertDictEqual({'a': 'aaaaa', 'b': 'bbbbb'}, self.menu.text_descriptions)
        self.assertDictEqual({'a': self.a, 'b': self.b}, self.menu.functions)


    def test_is_valid(self):
        self.assertTrue(self.menu.is_valid('a'))
        self.assertTrue(self.menu.is_valid('b'))


    def test_is_not_valid(self):
        self.assertFalse(self.menu.is_valid('aa'))
        self.assertFalse(self.menu.is_valid('c'))


    def test_get_action(self):
        self.assertEqual(self.a, self.menu.get_action('a'))
        self.assertEqual(self.b, self.menu.get_action('b'))


    def test_get_action_returns_none_if_not_in_menu(self):
        self.assertIsNone(self.menu.get_action('aa'))
        self.assertIsNone(self.menu.get_action('c'))


    def test_str(self):
        menu_string = 'a: aaaaa\nb: bbbbb'
        self.assertEqual(menu_string, str(self.menu))