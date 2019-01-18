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
    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100)
    authors = models.CharField(max_length=100)
    image = models.URLField(null=True, blank=True)
    objects = BookManager()

    @classmethod
    def from_volume(cls, **volume):
        """Create a Book instance from the data provided by the Google API.

        Book data returned by the Google Books API is described here:
        https://developers.google.com/books/docs/v1/reference/volumes#resource
        """

        # Smells!

        try:
            image = volume["volumeInfo"]["imageLinks"]["thumbnail"]
        except KeyError:
            # image = "https://books.google.com/googlebooks/images/no_cover_thumb.gif"
            image = None

        return cls(
            id=volume["id"],
            title=volume["volumeInfo"]["title"],
            authors=" & ".join(volume["volumeInfo"]["authors"]),
            image=image,
        )
