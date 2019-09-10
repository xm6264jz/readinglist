from unittest import TestCase
from unittest.mock import patch
import os 

import bookstore 
from bookstore import Book, BookStore

import ui
from menu import Menu


class TestUI(TestCase):
 
    @classmethod
    def setUpClass(cls):
        bookstore.db = os.path.join('database', 'test_books.db')
        BookStore.instance = None 



    @patch('builtins.input', side_effect=['a'])
    @patch('builtins.print')
    def test_display_menu_get_choice(self, mock_print, mock_input):
        menu = Menu()
        menu.add_option('a', 'aaa', lambda: None)
        menu.add_option('b', 'bbb', lambda: None)

        self.assertEqual('a', ui.display_menu_get_choice(menu))

        mock_print.assert_any_call(menu)


    @patch('builtins.print')
    def test_message(self, mock_print):
        ui.message('hello')
        mock_print.assert_called_with('hello')


    @patch('builtins.print')
    def test_show_books_empty(self, mock_print):
        books = []
        ui.show_books(books)
        mock_print.assert_called_with('No books to display')


    @patch('builtins.print')
    def test_show_books_list(self, mock_print):
        bk1 = Book('a', 'aaa')
        bk2 = Book('b', 'bbb')
        books = [bk1, bk2]
        ui.show_books(books)

        mock_print.assert_any_call(bk1)
        mock_print.assert_any_call(bk2)


    @patch('builtins.input', side_effect=['title', 'author'])
    def test_get_book_info(self, mock_input):
        book = ui.get_book_info()
        self.assertEqual('title', book.title)
        self.assertEqual('author', book.author)


    @patch('builtins.input', side_effect=['42'])
    def test_get_book_id(self, mock_input):
        self.assertEqual(42, ui.get_book_id())


    @patch('builtins.input', side_effect=['no', '-4', '0', 'sdfdf', 'pizza pizza pizza', '99 99 99', '9'])
    def test_get_book_id_rejects_non_positive_integer(self, mock_input):
        self.assertEqual(9, ui.get_book_id())


    @patch('builtins.input', side_effect=['read'])
    def test_get_read_value_read(self, mock_input):
        self.assertTrue(ui.get_read_value())


    @patch('builtins.input', side_effect=['not read'])
    def test_get_read_value_unread(self, mock_input):
        self.assertFalse(ui.get_read_value())


    @patch('builtins.input', side_effect=['not one of the options', 'pizza', '1234', 'Not', 'rea', 'read'])
    def test_get_read_value_validates(self, mock_input):
        self.assertTrue(ui.get_read_value())


    @patch('builtins.input', side_effect=['pizza'])
    @patch('builtins.print')
    def ask_question(self, mock_print, mock_input):
        self.assertEqual('pizza', ui.ask_question('What is your favorite food?'))
        mock_print.assert_called_with('What is your favorite food?')