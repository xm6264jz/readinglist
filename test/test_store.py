from unittest import TestCase

from bookstore import BookStore, BookError
from model import Book


class TestBookstore(TestCase):

    def setUp(self):
        self.BS = BookStore()
        self.clear_bookstore()


    def add_test_data(self):
        self.bk1 = Book('An Interesting Book', 'Ann Author', True)
        self.bk2 = Book('Booky Book Book', 'B. Bookwriter', False)
        self.bk3 = Book('Collection of words', 'Creative Creator')

        self.clear_bookstore()

        self.BS.add_book(self.bk1)
        self.BS.add_book(self.bk2)
        self.BS.add_book(self.bk3)


    def clear_bookstore(self):
        self.BS.delete_all_books()


    def test_singleton(self):
        bs = BookStore()
        bs2 = BookStore()
        self.assertEqual(bs, bs2)


    def test_add_book_empty_store(self):
        self.BS.delete_all_books()
        bk = Book('aa', 'aaa')
        self.BS.add_book(bk)
        self.assertTrue(self.BS.is_book_in_store(bk))
        self.assertEqual(1, self.BS.book_count())


    def test_add_book(self):
        self.add_test_data()
        book_count = self.BS.book_count()
        bk = Book('aa', 'bbbbb')
        self.BS.add_book(bk)
        self.assertTrue(self.BS.is_book_in_store(bk))
        self.assertEqual(book_count + 1, self.BS.book_count())


    def test_add_book_duplicate_errors(self):
        bk = Book('aa', 'aaa')
        self.BS.add_book(bk)
        with self.assertRaises(BookError):
            bk_dupe = Book('aa', 'aaa')
            self.BS.add_book(bk_dupe)


    def test_delete_book(self):
        self.add_test_data()
        count = self.BS.book_count()
        self.BS.delete_book(self.bk2)
        self.assertEqual(count - 1, self.BS.book_count())
        self.assertFalse(self.BS.is_book_in_store(self.bk2))


    def test_delete_book_not_in_store_errors(self):
        self.add_test_data()
        bk = Book('Not in store', 'Not in store')
        with self.assertRaises(BookError):
            self.BS.delete_book(bk)


    def test_delete_book_empty_list_errors(self):
        self.clear_bookstore()
        bk = Book('Not in store', 'Not in store')
        with self.assertRaises(BookError):
            self.BS.delete_book(bk)


    def test_delete_all_books(self):
        self.clear_bookstore()
        bk1 = Book('Not in store', 'Not in store')
        bk2 = Book('Whatever', 'Whatever')
        self.BS.add_book(bk1)
        self.BS.add_book(bk2)
        self.BS.delete_all_books()
        self.assertEqual(0, self.BS.book_count())


    def test_delete_all_books_empty(self):
        self.clear_bookstore()
        self.BS.delete_all_books()
        self.assertEqual(0, self.BS.book_count())


    def test_set_read_book_read(self):
        self.add_test_data()
        self.BS.set_book_read(self.bk1.id, True)


    def test_set_unread_book_read(self):
        self.add_test_data()
        self.BS.set_book_read(self.bk2.id, True)


    def test_set_read_book_unread(self):
        self.add_test_data()
        self.BS.set_book_read(self.bk1.id, False)


    def test_set_unread_book_unread(self):
        self.add_test_data()
        self.BS.set_book_read(self.bk2.id, False)


    def test_set_book_read_not_found_errors(self):
        bk = Book('Not in store', 'Not in store')
        with self.assertRaises(BookError):
            self.BS.set_book_read(bk.id, True)


    def test_is_book_in_store_present(self):
        self.add_test_data()
        self.assertTrue(self.BS.is_book_in_store(self.bk1))
        self.assertTrue(self.BS.is_book_in_store(self.bk2))
        self.assertTrue(self.BS.is_book_in_store(self.bk3))


    def test_is_book_in_store_not_present(self):
        not_in_store = Book('aaaa', 'bbbb')
        self.add_test_data()
        self.assertFalse(self.BS.is_book_in_store(not_in_store))


    def test_is_book_in_store_empty_list(self):
        self.clear_bookstore()
        not_in_store = Book('aaaa', 'bbbb')
        self.assertFalse(self.BS.is_book_in_store(not_in_store))


    def test_search_book_author_match(self):
        self.add_test_data()
        self.assertCountEqual([self.bk1], self.BS.book_search('Ann'))


    def test_search_book_title_match(self):
        self.add_test_data()
        self.assertCountEqual([self.bk1, self.bk2], self.BS.book_search('Book'))


    def test_search_book_not_found(self):
        self.add_test_data()
        self.assertEqual([], self.BS.book_search('Not in list'))


    def test_search_book_empty_store(self):
        self.clear_bookstore()
        self.assertEqual([], self.BS.book_search('Not in list'))


    def test_search_book_case_insensitive_title_match(self):
        self.add_test_data()
        self.assertCountEqual([self.bk1, self.bk2], self.BS.book_search('bOoK'))


    def test_search_book_case_insensitive_author_match(self):
        self.add_test_data()
        self.assertCountEqual([self.bk3], self.BS.book_search('cReAtOr'))


    def test_exact_match_found(self):
        self.add_test_data()
        bk = Book('Collection of words', 'Creative Creator')
        self.assertTrue(self.BS.exact_match(bk))


    def test_exact_match_not_found_author(self):
        self.add_test_data()
        bk = Book('Collection of words', 'Someone Else')
        self.assertFalse(self.BS.exact_match(bk))


    def test_exact_match_not_found_title(self):
        self.add_test_data()
        bk = Book('Collection of Stories', 'Creative Creator')
        self.assertFalse(self.BS.exact_match(bk))


    def test_exact_match_not_found_title_author(self):
        self.add_test_data()
        bk = Book('Collection of Cheese', 'Beyonce')
        self.assertFalse(self.BS.exact_match(bk))


    def test_exact_match_not_found_empty_store(self):
        bk = Book('Whatever', 'Whatever')
        self.clear_bookstore()
        self.assertFalse(self.BS.exact_match(bk))


    def test_get_books_by_read_read(self):
        self.add_test_data()
        read_books = self.BS.get_books_by_read_value(True)
        self.assertCountEqual([self.bk1], read_books)


    def test_get_books_by_read_unread(self):
        self.add_test_data()
        read_books = self.BS.get_books_by_read_value(False)
        self.assertCountEqual([self.bk2, self.bk3], read_books)



