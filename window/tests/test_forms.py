from django.test import TestCase

from window.forms import SearchForm


class FormTest(TestCase):
    def test_the_bible_is_a_valid_search(self):
        form = SearchForm({"query": "The Bible"})
        self.assertTrue(form.is_valid())

    def test_an_empty_query_is_invalid(self):
        form = SearchForm({"query": ""})
        self.assertFalse(form.is_valid())
