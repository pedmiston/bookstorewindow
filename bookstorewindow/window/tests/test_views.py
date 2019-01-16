from django.test import TestCase


class ViewTest(TestCase):
    def test_query_is_returned_in_the_response(self):
        query = "The Bible"
        response = self.client.post("/", {"query": query})
        html = response.content.decode("utf8")
        self.assertIn(query, html)
