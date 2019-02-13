from unittest import mock
from functools import partial
from pathlib import Path

from django.test import TestCase
from django.utils.text import slugify

from betamax import Betamax
from requests import Session


from google_books import api
from window.models import Book, create_books_from_volume_data


cassette_library_dir = "google_books/tests/fixtures"
if not Path(cassette_library_dir).is_dir():
    Path(cassette_library_dir).mkdir(parents=True)

with Betamax.configure() as config:
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
        results = api.search_volumes(query, session=self.session)
        self.assertTrue(len(results) > 0)

    def test_create_book_instances_from_book_data(self):
        query = "The Bible"
        self.vcr.use_cassette(slugify(query))
        volume_data = api.search_volumes(query, session=self.session)
        books = create_books_from_volume_data(volume_data)
        self.assertTrue(all(book.title != "" for book in books))

    def test_books_have_authors(self):
        query = "Sapiens: A Brief History of Humankind"
        self.vcr.use_cassette(slugify(query))
        volume_data = api.search_volumes(query, session=self.session)
        books = create_books_from_volume_data(volume_data)
        self.assertGreater(len(books), 0)
        for book in books:
            self.assertNotEqual(book.authors, "")

    def test_books_have_expected_google_book_ids(self):
        query = "Sapiens: A Brief History of Humankind"
        self.vcr.use_cassette(slugify(query))
        volume_data = api.search_volumes(query, session=self.session)
        books = create_books_from_volume_data(volume_data)
        self.assertEquals(books[0].google_book_id, "FmyBAwAAQBAJ")


class ViewTest(TestCase):
    def setUp(self):
        self.session = Session()
        self.vcr = Betamax(self.session)
        self.vcr.start()

        self.search_volumes = partial(
            api.search_volumes, session=self.session
        )

    def tearDown(self):
        self.vcr.stop()

    def test_query_is_returned_in_the_response(self):
        query = "The Bible"
        self.vcr.use_cassette(slugify(query))
        with mock.patch("window.views.search_volumes", self.search_volumes):
            response = self.client.post("/", {"query": query})
            html = response.content.decode("utf8")
            self.assertIn(query, html)

    def test_author_is_included_in_the_response(self):
        query = "Sapiens: A Brief History of Humankind"
        author = "Yuval Noah Harari"
        self.vcr.use_cassette(slugify(query))
        with mock.patch("window.views.search_volumes", self.search_volumes):
            response = self.client.post("/", {"query": query})
            html = response.content.decode("utf8")
            self.assertIn(author, html)

    def test_book_image_is_included_in_the_response(self):
        query = "The Plague"
        self.vcr.use_cassette(slugify(query))
        with mock.patch("window.views.search_volumes", self.search_volumes):
            response = self.client.post("/", {"query": query})
            html = response.content.decode("utf8")
            self.assertIn("<img", html)
