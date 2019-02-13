import logging
import json

from django.db import models
from django.core.exceptions import ValidationError

from . import google_books_api

logger = logging.getLogger(__name__)


def create_books_from_volume_data(volume_data):
    """Create Book instances from a query to the Google Books API."""
    books = []
    for volume in volume_data:
        try:
            book = Book.from_volume_data(volume)
        except BookCreationError as err:
            logger.error(err)
            continue

        try:
            book.full_clean()
        except ValidationError:
            book = Book.objects.get(google_book_id=book.google_book_id)
        else:
            book.save()

        books.append(book)

    return books


class Book(models.Model):
    google_book_id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100)
    authors = models.CharField(max_length=100)
    image = models.URLField()
    publisher = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, blank=True)

    @classmethod
    def from_volume_data(cls, volume):
        """Create a Book instance from the data provided by the Google Books API.

        The volume data returned by the Google Books API is described here:
        https://developers.google.com/books/docs/v1/reference/volumes#resource
        """

        # Smells!

        try:
            google_book_id = volume["id"]
            title = volume["volumeInfo"]["title"]
            authors = " & ".join(volume["volumeInfo"]["authors"])
            publisher = volume["volumeInfo"]["publisher"]
        except KeyError as err:
            raise BookCreationError(err)

        try:
            subtitle = volume["volumeInfo"]["subtitle"]
        except KeyError as err:
            subtitle = ""

        try:
            image = volume["volumeInfo"]["imageLinks"]["thumbnail"]
        except KeyError:
            image = "https://books.google.com/googlebooks/images/no_cover_thumb.gif"

        return cls(google_book_id=google_book_id, title=title, authors=authors, image=image, publisher=publisher, subtitle=subtitle)


class BookCreationError(Exception):
    pass
