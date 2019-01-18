from django.db import models

from . import google_books_api


class BookManager(models.Manager):
    def search(self, query, session=None):
        """Create a book instance for each result of the query.

        Returns an empty list if no results are found.
        """
        book_data = google_books_api.search(query, session=session)
        return [Book.from_volume(**datum) for datum in book_data]


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.CharField(max_length=100)
    objects = BookManager()

    @classmethod
    def from_volume(cls, **volume):
        """Create a Book instance from the data provided by the Google API.

        Book data returned by the Google Books API is described here:
        https://developers.google.com/books/docs/v1/reference/volumes#resource
        """

        # Smells!
        return cls(
            title=volume["volumeInfo"]["title"],
            authors=" & ".join(volume["volumeInfo"]["authors"]),
        )
