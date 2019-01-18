from django.test import TestCase


class ViewTest(TestCase):
    def test_query_is_returned_in_the_response(self):
        query = "The Bible"
        response = self.client.post("/", {"query": query})
        html = response.content.decode("utf8")
        self.assertIn(query, html)

    def test_author_is_included_in_the_response(self):
        query = "Sapiens: A Brief History of Humankind"
        author = "Yuval Noah Harari"
        response = self.client.post("/", {"query": query})
        html = response.content.decode("utf8")
        self.assertIn(author, html)
