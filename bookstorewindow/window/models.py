from django.db import models


class BookManager(models.Manager):
    def search(self, query):
        return [Book(title=query)]


class Book(models.Model):
    title = models.CharField(max_length=100)
    objects = BookManager()
