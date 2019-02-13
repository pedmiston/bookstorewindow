from django.test import TestCase


class ViewTest(TestCase):
    def test_window_template_is_used_on_homepage(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "window/index.html")
