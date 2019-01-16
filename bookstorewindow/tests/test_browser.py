from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver


class BrowserTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_window_has_search_input(self):
        self.browser.get(self.live_server_url)
        input = self.browser.find_element_by_tag_name("input")
        self.assertEquals(input.get_attribute("name"), "search")
