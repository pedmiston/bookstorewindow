from django.test import TestCase
from django.core.exceptions import ValidationError

from window.models import Book


class ModelTest(TestCase):
    def test_required_data_for_books(self):
        book = Book()
        with self.assertRaises(ValidationError):
            book.full_clean()

        book = Book(
            google_book_id="1",
            title="The Bible",
            authors="Paul",
            publisher="Oxford",
            image="http://internet.com/bible.png",
            subtitle="Version 1"
        )
        book.full_clean()  # does not raise
