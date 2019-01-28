import logging
import json

from django.db import models
from django.core.exceptions import ValidationError

from . import google_books_api

logger = logging.getLogger(__name__)


def create_books_from_volume_data(volume_data):
    """Create books out of the results of a query to the Google Books API.

    Some queries return volumes that are for practical purposes
    identical, even though the Google Books API has indexed them
    as separate entities. For this reason, books may have one
    or more volumes associated with them.
    """
    books = []

    for volume in volume_data:
        try:
            book = Book.from_volume_data(volume)
        except BookCreationError as err:
            logger.error(err)
            continue

        try:
            book.full_clean()
        except ValidationError as err:
            book = Book.objects.get(title=book.title, authors=book.authors)
        else:
            book.save()

        volume = Volume.from_volume_data(volume)
        book.volumes.add(volume, bulk=False)

        if book not in books:
            books.append(book)

    return books


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.CharField(max_length=100)
    image = models.URLField(blank=True)
    publisher = models.CharField(max_length=100, blank=True)
    subtitle = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ("title", "authors")

    @classmethod
    def from_volume_data(cls, volume):
        """Create a Book instance from the data provided by the Google Books API.

        The volume data returned by the Google Books API is described here:
        https://developers.google.com/books/docs/v1/reference/volumes#resource
        """

        # Smells!

        try:
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

        return cls(title=title, authors=authors, image=image, publisher=publisher, subtitle=subtitle)


class Volume(models.Model):
    google_book_id = models.CharField(max_length=100, primary_key=True)
    volume_info = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="volumes")

    class Meta:
        ordering = ["google_book_id"]

    @classmethod
    def from_volume_data(cls, volume):
        """Create a Book instance from the data provided by the Google Books API.

        The volume data returned by the Google Books API is described here:
        https://developers.google.com/books/docs/v1/reference/volumes#resource
        """
        google_book_id = volume["id"]
        volume_info = json.dumps(volume)
        return cls(google_book_id=google_book_id, volume_info=volume_info)


class BookCreationError(Exception):
    pass
