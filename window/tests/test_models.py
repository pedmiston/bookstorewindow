from django.test import TestCase
from django.core.exceptions import ValidationError

from window.models import Book


class ModelTest(TestCase):
    def test_required_data_for_books(self):
        book = Book()
        with self.assertRaises(ValidationError):
            book.full_clean()

        book = Book(title="The Bible", authors="Paul")
        book.full_clean()  # does not raise

    def test_cant_make_two_books_with_same_title_and_authors(self):
        book1 = Book(title="Hello, World", authors="Pierce")
        book1.save()
        book2 = Book(title="Hello, World", authors="Pierce")
        with self.assertRaises(ValidationError):
            book2.full_clean()
