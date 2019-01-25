from unittest import mock
from functools import partial
from pathlib import Path

from django.test import TestCase
from django.utils.text import slugify

from requests import Session
from betamax import Betamax

from window import google_books_api


with Betamax.configure() as config:
    cassette_library_dir = "window/tests/fixtures/cassettes"
    if not Path(cassette_library_dir).is_dir():
        Path(cassette_library_dir).mkdir(parents=True)
    config.cassette_library_dir = cassette_library_dir


class ViewTest(TestCase):
    def setUp(self):
        self.session = Session()
        self.vcr = Betamax(self.session)
        self.vcr.start()

        self.search_volumes = partial(google_books_api.search_volumes, session=self.session)

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
