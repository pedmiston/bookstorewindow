from django.test import TestCase
from django.core.exceptions import ValidationError

from model_mommy import mommy

from window.models import Book, create_books_from_volume_data, BookCreationError, NO_COVER_THUMB


class ModelTest(TestCase):
    def test_required_data_for_creating_a_book(self):
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

    def test_subtitle_is_optional(self):
        book = mommy.prepare("window.Book", subtitle="")
        book.full_clean()  # does not raise

    def test_books_are_fetched_from_db_rather_than_recreated(self):
        books = mommy.make("window.Book", _quantity=5)
        volume_data = [{"id": book.google_book_id} for book in books]
        new_books = create_books_from_volume_data(volume_data)
        self.assertEqual(books, new_books)

    def test_creating_a_book_from_faulty_volume_data_raises_error(self):
        with self.assertRaises(BookCreationError):
            Book.from_volume_data({})

    def test_creating_a_book_without_thumbnail_gets_no_cover_image(self):
        volume = {
            "id": "1",
            "volumeInfo": {
                "title": "A Title",
                "authors": ["Me", "Myself"],
                "publisher": "New York",
            }
        }
        book = Book.from_volume_data(volume)
        self.assertEquals(book.image, NO_COVER_THUMB)

        volume["volumeInfo"]["imageLinks"] = {"thumbnail": ""}
        book = Book.from_volume_data(volume)
        self.assertEquals(book.image, NO_COVER_THUMB)
