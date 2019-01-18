from django.test import TestCase
from django.core.exceptions import ValidationError

from window.models import Book


class ModelTest(TestCase):
    def test_book_manager_returns_list_of_books(self):
        query = "The Bible"
        results = Book.objects.search(query)
        self.assertTrue(len(results) > 0)
        self.assertIsInstance(results[0], Book)

    def test_required_data_for_books(self):
        book = Book()
        with self.assertRaises(ValidationError):
            book.full_clean()

        book = Book(title="The Bible", authors="Paul", id="123")
        book.full_clean()  # does not raise
