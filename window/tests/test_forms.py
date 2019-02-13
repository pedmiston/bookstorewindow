from django.test import TestCase

from window.forms import SearchForm


class FormTest(TestCase):
    def test_a_valid_search(self):
        form = SearchForm({"query": "The Bible"})
        self.assertTrue(form.is_valid())

    def test_an_empty_query_is_invalid(self):
        form = SearchForm({"query": ""})
        self.assertFalse(form.is_valid())

    def test_a_bad_query_is_still_valid(self):
        form = SearchForm({"query": "aldfkjadfkajsdlfaasldfj"})
        self.assertTrue(form.is_valid())
