
class BookStore:

    """ Singleton class to hold and manage a list of Books. """

    instance = None

    class __BookStore:
        def __init__(self):
            self._books = []

        def add_book(self, book):
            """ Adds book to store. Should error if a book with exact author and title is already in the store.
             :param book the book to add"""
            # TODO raise BookError if book with same author and title is already in list. Don't add the new book. Use the exact_match function
            self._books.append(book)


        def delete_book(self, book):
            """ Removes book from store. Raises BookError if book not in store. """
            try:
                self._books.remove(book)
            except ValueError:
                raise BookError('Tried to delete book that doesn\'t exist')


        def delete_all_books(self):
            """ Clears the book list """
            self._books = []


        def set_book_read(self, id, read):
            """ Changes whether a book has been read or not
            :param id the ID of the book to change the read status
            :param read True for book has been read, False otherwise
            """
            book = self.get_book_by_id(id)
            book.read = read
            # TODO raise BookError if book not found. Hint: get_book_by_id returns None if book is not found.


        def exact_match(self, search_book):
            """ Searches bookstore for a book with exact same title and author. Not case sensitive.
             :param search_book: the book to search for
             :returns: True if a book with same author and title are found in the store, false otherwise. """
            matches = [book for book in self._books if
                       book.author.lower() == search_book.author.lower()
                       and book.title.lower() == search_book.title.lower()]
            return len(matches) > 0


        def is_book_in_store(self, book):
            """Looks for a book object in a store. Will not identify different book objects with same author/title
            :returns True if this specific Book object is in the store."""

            return book in self._books


        def get_book_by_id(self, id):
            """ Searches list for Book with given ID,
            :param id the ID to search for
            :returns the book, if found, or None if book not found.
            """
            matches = [book for book in self._books if book.id == id]
            if matches:
                return matches[0]


        def book_search(self, term):
            """ Searches the store for books whose author or title contain a search term.
            Makes partial matches, so a search for 'Row' will match a book with author='JK Rowling'; a book with title='Rowing For Dummies'
            :param term the search term
            :returns a list of books with author or title that match the search term.
            """
            # TODO make this case-insensitive. So 'ROWLING' is a match for a book with author = 'jk rowling'
            return [book for book in self._books if term in book.title or term in book.author]


        def get_books_by_read_value(self, read):
            """ Get a list of books that have been read, or list of books that have not been read.
            :param read True for books that have been read, False for books that have not been read
            :returns all books with the read value.
            """
            return [book for book in self._books if book.read == read]


        def get_all_books(self):
            """ :returns entire booklist """
            return self._books


        def book_count(self):
            """ :returns the number of books in the store """
            return len(self._books)


    def __new__(cls):
        if not BookStore.instance:
            BookStore.instance = BookStore.__BookStore()
        return BookStore.instance


    def __getattr__(self, name):
        return getattr(self.instance, name)


    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)



class BookError(Exception):
    """ For BookStore errors. """
    pass
