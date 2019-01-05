from unittest import TestCase
from model import Book, Counter


class TestCounter(TestCase):

    def test_counter(self):
        Counter.reset_counter()
        self.assertEqual(1, Counter.get_counter())
        self.assertEqual(2, Counter.get_counter())


class TestBook(TestCase):

    def test_create_book_id_increases(self):
        Counter.reset_counter()

        bk = Book('Title', 'Author')
        self.assertEqual(1, bk.id)

        bk2 = Book('Title2', 'Author2')
        self.assertEqual(2, bk2.id)

        bk3 = Book('Title3', 'Author3')
        self.assertEqual(3, bk3.id)


    def test_create_book_title_author_read(self):
        bk = Book('Title', 'Author', True)
        self.assertEqual(bk.title, 'Title')
        self.assertEqual(bk.author, 'Author')
        self.assertTrue(bk.read)


    def test_create_book_default_unread(self):
        bk = Book('Title', 'Author')
        self.assertFalse(bk.read)


    def test_string(self):
        Counter.reset_counter()
        bk = Book('AAAA', 'BBBB', True)
        self.assertIn('1', str(bk))   # ID should be 1
        self.assertIn('AAAA', str(bk))
        self.assertIn('BBBB', str(bk))
        self.assertIn('You have read', str(bk))

