from django.test import TestCase
from django.utils.text import slugify
from betamax import Betamax
from requests import Session


from window import google_books_api
from window.models import Book


with Betamax.configure() as config:
    config.cassette_library_dir = "window/tests/fixtures/cassettes"


class GoogleAPITest(TestCase):
    def setUp(self):
        self.session = Session()
        self.vcr = Betamax(self.session)
        self.vcr.start()

    def tearDown(self):
        self.vcr.stop()

    def test_searching_for_a_book_returns_a_list_of_dicts(self):
        query = "The Bible"
        self.vcr.use_cassette(slugify(query))
        results = google_books_api.search(query, session=self.session)
        self.assertTrue(len(results) > 0)

    def test_create_book_instances_from_book_data(self):
        query = "The Bible"
        self.vcr.use_cassette(slugify(query))
        books = Book.objects.search(query, session=self.session)
        self.assertTrue(all(book.title != "" for book in books))

    def test_books_have_authors(self):
        query = "Sapiens: A Brief History of Humankind"
        self.vcr.use_cassette(slugify(query))
        books = Book.objects.search(query, session=self.session)
        for book in books:
            if book.title == query:
                self.assertEqual(book.authors, "Yuval Noah Harari")

    def test_books_have_ids(self):
        query = "Sapiens: A Brief History of Humankind"
        self.vcr.use_cassette(slugify(query))
        books = Book.objects.search(query, session=self.session)
        best_result = books[0]
        self.assertEquals(best_result.id, "FmyBAwAAQBAJ")
