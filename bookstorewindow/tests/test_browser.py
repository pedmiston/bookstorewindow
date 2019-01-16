from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class BrowserTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox()

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
        assert len(results) > 0
