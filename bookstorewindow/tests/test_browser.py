import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class BrowserTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox()

        # Configure webdriver to wait for page reloads
        cls.browser.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        self.browser.get(self.live_server_url)

    def test_window_has_search_input(self):
        self.browser.find_element_by_id("id_query")

    def test_user_can_search_for_the_bible(self):
        search = self.browser.find_element_by_id("id_query")
        search.send_keys("The Bible")
        search.submit()

        results = self.browser.find_elements_by_tag_name("li")
        self.assertTrue(len(results) > 0)

    def test_user_can_click_on_a_link_to_learn_more_about_the_book(self):
        search = self.browser.find_element_by_id("id_query")
        search.send_keys("Sapiens: A Brief History of Humankind")
        search.submit()

        result = self.browser.find_elements_by_tag_name("li")[0]
        link = result.find_element_by_class_name("google-book-page").get_attribute("href", "")
        self.assertIn("books.google.com/books?id=", link)
