from unittest import TestCase
from unittest.mock import patch
from model import Book, Counter
from bookstore import BookStore
import main


class TestWishList(TestCase):

    """
    menu.add_option('1', 'Add Book', add_book)
    menu.add_option('2', 'Search For Book', search_book)
    menu.add_option('3', 'Show Unread Books', show_unread_books)
    menu.add_option('4', 'Show Read Books', show_read_books)
    menu.add_option('5', 'Show All Books', show_all_books)
    menu.add_option('6', 'Change Book Read Status', change_read)
    """

    def setUp(self):
        self.store = BookStore()
        self.store.delete_all_books()
        Counter.reset_counter()


    def add_test_data(self):
        self.bk1 = Book('the title', 'the author', False)
        self.bk2 = Book('what the book is called', 'the writer', True)
        self.bk3 = Book('fascinating', 'the author', True)
        self.bk4 = Book('brilliant', 'schrodinger', False)

        self.store.add_book(self.bk1)
        self.store.add_book(self.bk2)
        self.store.add_book(self.bk3)
        self.store.add_book(self.bk4)


    @patch('builtins.input', side_effect=['1', 'Title', 'Author', 'Q'])
    @patch('builtins.print')
    def test_add_book(self, mock_print, mock_input):
        main.main()
        # reset counter and make book that mimics the one expected to be created
        Counter.reset_counter()
        expected_book = Book('Title', 'Author', False)
        all_books = self.store.get_all_books()
        self.assertEqual(expected_book, all_books[0])


    @patch('builtins.input', side_effect=['1', 'Title', 'Author', '1', 'title', 'author', 'Q'])
    @patch('builtins.print')
    def test_add_book_prevent_duplicates(self, mock_print, mock_input):
        main.main()
        # reset counter and make book that mimics the first one expected to be created
        Counter.reset_counter()
        expected_book = Book('Title', 'Author', False)
        all_books = self.store.get_all_books()
        self.assertEqual(expected_book, all_books[0])
        self.assertEqual(1, self.store.book_count())


    @patch('builtins.input', side_effect=['2', 'call', 'Q'])  # match bk2
    @patch('builtins.print')
    def test_search_for_book_found(self, mock_print, mock_input):
        self.add_test_data()
        main.main()
        mock_print.assert_any_call(self.bk2)


    @patch('builtins.input', side_effect=['2', 'the author', 'Q'])  # Partial match bk1 and bk3
    @patch('builtins.print')
    def test_search_for_book_multiple_books_found(self, mock_print, mock_input):
        self.add_test_data()
        # assert bk1 and bk3 is printed
        main.main()
        mock_print.assert_any_call(self.bk1)
        mock_print.assert_any_call(self.bk3)


    @patch('builtins.input', side_effect=['2', 'jk rowling', 'Q'])  # No match
    @patch('builtins.print')
    def test_search_for_book_not_found(self, mock_print, mock_input):
        self.add_test_data()
        main.main()
        mock_print.assert_any_call('No books to display')


    @patch('builtins.input', side_effect=['3', 'Q'])
    @patch('builtins.print')
    def test_show_unread_books(self, mock_print, mock_input):
        self.add_test_data()
        main.main()
        mock_print.assert_any_call(self.bk1)
        mock_print.assert_any_call(self.bk4)


    @patch('builtins.input', side_effect=['4', 'Q'])
    @patch('builtins.print')
    def test_show_read_books(self, mock_print, mock_input):
        self.add_test_data()
        main.main()
        mock_print.assert_any_call(self.bk2)
        mock_print.assert_any_call(self.bk3)


    @patch('builtins.input', side_effect=['5', 'Q'])
    @patch('builtins.print')
    def test_show_all_books(self, mock_print, mock_input):
        self.add_test_data()

        main.main()
        mock_print.assert_any_call(self.bk1)
        mock_print.assert_any_call(self.bk2)
        mock_print.assert_any_call(self.bk3)
        mock_print.assert_any_call(self.bk4)


    @patch('builtins.input', side_effect=['6', '4', 'read', 'Q'])  # Change book Id 4 to read
    @patch('builtins.print')
    def test_change_book_read_status(self, mock_print, mock_input):
        self.add_test_data()
        main.main()
        self.assertTrue(self.bk4.read)


    @patch('builtins.input', side_effect=['6', '3', 'not read', 'Q'])  # Change book Id 3 to unread
    @patch('builtins.print')
    def test_change_book_read_status_unread(self, mock_print, mock_input):
        self.add_test_data()
        main.main()
        self.assertFalse(self.bk3.read)


    @patch('builtins.input', side_effect=['6', '42', 'not read', 'Q'])  # Change book Id 42 (not found) to unread,
    @patch('builtins.print')
    def test_change_book_read_status_book_not_found(self, mock_print, mock_input):
        self.add_test_data()
        main.main()
        # Not crash? All's well.


    @patch('builtins.input', side_effect=['7', '3', 'Q'])  # Delete book ID 3
    @patch('builtins.print')
    def test_delete_book_in_list(self, mock_print, mock_input):
        self.add_test_data()
        main.main()
        self.assertNotIn(self.bk3, self.store.get_all_books())


    @patch('builtins.input', side_effect=['7', '42', 'Q'])  # Delete book ID 42, not a book in list
    @patch('builtins.print')
    def test_delete_book_not_found_in_list(self, mock_print, mock_input):
        self.add_test_data()
        main.main()
        self.assertEqual(4, self.store.book_count())
