from unittest import TestCase
import os 

import bookstore
from bookstore import Book, BookStore


class TestBook(TestCase):

    @classmethod
    def setUpClass(cls):
        bookstore.db = os.path.join('database', 'test_books.db')
        BookStore.instance = None 


    def test_create_book_default_unread(self):
        bk = Book('Title', 'Author')
        self.assertFalse(bk.read)


    def test_string(self):
        bk = Book('AAAA', 'BBBB', True)
        self.assertIn('AAAA', str(bk))
        self.assertIn('BBBB', str(bk))
        self.assertIn('You have read', str(bk))


    def test_save_add_to_db(self):
        bk = Book('AAA', 'BBB', True)
        bk.save()
        self.assertIsNotNone(bk.id)  # Check book has ID
        store = BookStore()
        self.assertEqual(bk, store.get_book_by_id(bk.id))
        self.assertTrue(store.exact_match(bk))
        

    def test_save_update_changes_to_db(self):
        
        bk = Book('CCC', 'DDD', True)
        bk.save()
        
        # Change some attributes and save 
        bk.author = 'EEE'
        bk.title = 'FFF'
        bk.read = False 

        bk.save() 

        store = BookStore()
        
        # Check DB has same data as bk Book object 
        self.assertEqual(bk, store.get_book_by_id(bk.id))
        self.assertTrue(bk, store.exact_match(bk))
        

