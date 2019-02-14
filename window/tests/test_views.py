from unittest import mock

from django.test import TestCase

from model_mommy import mommy


class ViewTest(TestCase):
    def test_window_template_is_used_on_homepage(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "window/index.html")

    @mock.patch("window.views.search_volumes")
    def test_posting_a_query_searches_the_google_books_api(self, search_volumes):
        self.client.post("/", {"query": "The Lorax"})
        search_volumes.assert_called_with("The Lorax")

    @mock.patch("window.views.search_volumes")
    @mock.patch("window.views.create_books_from_volume_data")
    def test_posting_a_query_returns_a_list_of_books(
        self, create_books_from_volume_data, search_volumes
    ):
        n_books = 4
        books = mommy.make("window.Book", _quantity=n_books)
        create_books_from_volume_data.return_value = books
        response = self.client.post("/", {"query": "Hamlet"})
        self.assertIn("books", response.context)
        self.assertEqual(len(response.context["books"]), n_books)
        self.assertEqual(response.context["books"], books)

    @mock.patch("window.views.search_volumes")
    @mock.patch("window.views.create_books_from_volume_data")
    def test_a_query_that_doesnt_have_any_books_comes_back_with_errors(
        self, create_books_from_volume_data, search_volumes
    ):
        create_books_from_volume_data.return_value = []
        response = self.client.post("/", {"query": "Hamlet"})
        form = response.context["form"]
        self.assertEqual(len(form.errors), 1)
