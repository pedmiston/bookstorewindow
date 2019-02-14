import logging
import json

from django.db import models
from django.core.exceptions import ValidationError


logger = logging.getLogger(__name__)


NO_COVER_THUMB = "https://books.google.com/googlebooks/images/no_cover_thumb.gif"


def create_books_from_volume_data(volume_data):
    """Create Book instances from a query to the Google Books API."""
    books = []
    for volume in volume_data:
        # First try to get the book from the DB if it exists
        try:
            book = Book.objects.get(google_book_id=volume["id"])
        except Book.DoesNotExist:
            pass
        else:
            # The book was retrieved from the DB
            books.append(book)
            continue

        # Then try to create a book from the volume data
        try:
            book = Book.from_volume_data(volume)
            book.full_clean()
        except (BookCreationError, ValidationError) as err:
            # Couldn't make a book
            logger.error(err)
            continue
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
    description = models.TextField(blank=True)

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
            image = NO_COVER_THUMB

        if not image:
            image = NO_COVER_THUMB

        try:
            description = volume["volumeInfo"]["description"]
        except KeyError:
            description = ""

        return cls(
            google_book_id=google_book_id,
            title=title,
            authors=authors,
            image=image,
            publisher=publisher,
            subtitle=subtitle,
            description=description,
        )


class BookCreationError(Exception):
    pass
