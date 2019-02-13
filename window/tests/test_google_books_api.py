from pathlib import Path

from django.test import TestCase
from django.utils.text import slugify
from betamax import Betamax
from requests import Session


from window import google_books_api
from window.models import Book, create_books_from_volume_data


with Betamax.configure() as config:
    cassette_library_dir = "window/tests/fixtures/cassettes"
    if not Path(cassette_library_dir).is_dir():
        Path(cassette_library_dir).mkdir(parents=True)
    config.cassette_library_dir = cassette_library_dir


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
        results = google_books_api.search_volumes(query, session=self.session)
        self.assertTrue(len(results) > 0)

    def test_create_book_instances_from_book_data(self):
        query = "The Bible"
        self.vcr.use_cassette(slugify(query))
        volume_data = google_books_api.search_volumes(query, session=self.session)
        books = create_books_from_volume_data(volume_data)
        self.assertTrue(all(book.title != "" for book in books))

    def test_books_have_authors(self):
        query = "Sapiens: A Brief History of Humankind"
        self.vcr.use_cassette(slugify(query))
        volume_data = google_books_api.search_volumes(query, session=self.session)
        books = create_books_from_volume_data(volume_data)
        for book in books:
            if book.title == query:
                self.assertEqual(book.authors, "Yuval Noah Harari")

    def test_books_have_volumes(self):
        query = "Sapiens: A Brief History of Humankind"
        self.vcr.use_cassette(slugify(query))
        volume_data = google_books_api.search_volumes(query, session=self.session)
        books = create_books_from_volume_data(volume_data)
        self.assertEquals(books[0].google_book_id, "FmyBAwAAQBAJ")
