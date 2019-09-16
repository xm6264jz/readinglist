from unittest import TestCase
import os 

import bookstore 
from bookstore import Book, BookStore, BookError

class TestBookstore(TestCase):

    @classmethod
    def setUpClass(cls):
        bookstore.db = os.path.join('database', 'test_books.db')
        BookStore.instance = None 


    def setUp(self):
        self.BS = BookStore()
        self.clear_bookstore()


    def add_test_data(self):
        self.clear_bookstore()

        self.bk1 = Book('An Interesting Book', 'Ann Author', True)
        self.bk2 = Book('Booky Book Book', 'B. Bookwriter', False)
        self.bk3 = Book('Collection of words', 'Creative Creator')

        self.bk1.save()
        self.bk2.save()
        self.bk3.save()


    def clear_bookstore(self):
        self.BS.delete_all_books()


    def test_singleton(self):
        bs = BookStore()
        bs2 = BookStore()
        self.assertEqual(bs, bs2)


    def test_add_book_empty_store(self):        
        bk = Book('aa', 'aaa')
        bk.save()
        self.assertTrue(self.BS.exact_match(bk))
        self.assertEqual(1, self.BS.book_count())


    def test_add_book_store_with_books_in(self):
        self.add_test_data()
        book_count = self.BS.book_count()
        bk = Book('aa', 'bbbbb')
        bk.save()
        self.assertTrue(self.BS.exact_match(bk))
        self.assertEqual(book_count + 1, self.BS.book_count())


    def test_add_book_duplicate_errors(self):
        bk = Book('aa', 'aaa')
        bk.save()
        with self.assertRaises(BookError):
            bk_dupe = Book('aa', 'aaa')
            bk_dupe.save()
       

    def test_add_book_duplicate_errors_case_insensitive(self):
        bk = Book('a', 'a')
        bk.save()
        with self.assertRaises(BookError):
            bk_dupe = Book('a', 'A')
            bk_dupe.save()


    def test_get_book_by_id_found(self):
        self.add_test_data()
        result = self.BS.get_book_by_id(self.bk1.id)
        self.assertEqual(result, self.bk1)


    def test_get_book_by_id_not_found(self):
        # This test fails - student should fix 
        self.add_test_data()
        result = self.BS.get_book_by_id(-1)
        self.assertIsNone(result)


    def test_delete_book_object(self):
        self.add_test_data()
        count = self.BS.book_count()
        self.bk2.delete()
        self.assertEqual(count - 1, self.BS.book_count())
        self.assertFalse(self.BS.exact_match(self.bk2))


    def test_delete_book_not_in_store_errors(self):
        self.add_test_data()
        bk = Book('Not in store', 'Not in store')
        with self.assertRaises(BookError):
            bk.delete()


    def test_delete_book_empty_list_errors(self):
        bk = Book('Not in store', 'Not in store')
        with self.assertRaises(BookError):
            bk.delete()


    def test_delete_all_books(self):
        bk1 = Book('Not in store', 'Not in store')
        bk2 = Book('Whatever', 'Whatever')
        bk1.save()
        bk2.save()

        self.BS.delete_all_books()
        self.assertEqual(0, self.BS.book_count())


    def test_delete_all_books_empty(self):
        self.BS.delete_all_books()
        self.assertEqual(0, self.BS.book_count())


    def test_count_books(self):
        self.add_test_data()
        count = self.BS.book_count()
        self.assertEqual(3, count)


    def test_set_read_book_read(self):
        self.add_test_data()
        self.bk1.read = True
        self.bk1.save()
       
        bk1_from_store = self.BS.get_book_by_id(self.bk1.id)
        self.assertTrue(bk1_from_store.read)


    def test_set_unread_book_read(self):
        self.add_test_data()
        self.bk2.read = True 
        self.bk2.save()
        
        bk2_from_store = self.BS.get_book_by_id(self.bk2.id)
        self.assertTrue(bk2_from_store.read)


    def test_set_read_book_unread(self):
        self.add_test_data()
      
        self.bk1.read = False
        self.bk1.save()

        bk1_from_store = self.BS.get_book_by_id(self.bk1.id)
        self.assertFalse(bk1_from_store.read)


    def test_set_unread_book_unread(self):
        self.add_test_data()
        self.bk2.read = False 
        self.bk2.save()

        bk2_from_store = self.BS.get_book_by_id(self.bk2.id)
        self.assertFalse(bk2_from_store.read)


    def test_get_all_books(self):
        self.add_test_data()
        self.assertCountEqual([self.bk1, self.bk2, self.bk3], self.BS.get_all_books())


    def test_is_book_in_store_present(self):
        self.add_test_data()
        self.assertTrue(self.BS.exact_match(self.bk1))
        self.assertTrue(self.BS.exact_match(self.bk2))
        self.assertTrue(self.BS.exact_match(self.bk3))


    def test_is_book_in_store_not_present(self):
        not_in_store = Book('aaaa', 'bbbb')
        self.add_test_data()
        self.assertFalse(self.BS.exact_match(not_in_store))


    def test_is_book_in_store_empty_list(self):
        self.clear_bookstore()
        not_in_store = Book('aaaa', 'bbbb')
        self.assertFalse(self.BS.exact_match(not_in_store))


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



