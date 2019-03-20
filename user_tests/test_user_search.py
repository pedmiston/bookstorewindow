import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UserSearchTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        # Get the path to the chromedriver if it is provided in the environment.
        # Otherwise, chromedriver is expected on the user's PATH.
        chromedriver = os.environ.get("CHROMEDRIVER", "chromedriver")

        cls.browser = webdriver.Chrome(chromedriver, chrome_options=options)

        # Configure webdriver to wait for page reloads
        cls.browser.implicitly_wait(5)

        # Check if running against a staging server
        staging_server = os.environ.get("STAGING_SERVER")
        if staging_server:
            cls.live_server_url = staging_server

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        self.browser.get(self.live_server_url)

    def test_window_has_search_input(self):
        search_input = self.browser.find_element_by_id("id_query")
        self.assertEqual(search_input.tag_name, "input")

    def test_user_searches_for_a_book(self):
        search = self.browser.find_element_by_id("id_query")
        search.send_keys("The Bible")
        search.submit()

        results = self.browser.find_elements_by_css_selector("div.book")
        self.assertTrue(len(results) > 0)

    def test_user_sees_publisher_of_a_book(self):
        search = self.browser.find_element_by_id("id_query")
        search.send_keys("Statistical Rethinking")
        search.submit()

        first_result = self.browser.find_element_by_css_selector("div.book")
        publisher = first_result.find_element_by_css_selector("div.publisher").text
        self.assertEquals(publisher, "CRC Press")

    def test_user_learns_more_about_the_book(self):
        search = self.browser.find_element_by_id("id_query")
        search.send_keys("Sapiens: A Brief History of Humankind")
        search.submit()

        result = self.browser.find_elements_by_css_selector("div.book")[0]

        # User clicks the "Description" button
        link = result.find_element_by_class_name("google-book-page")
        self.assertFalse(link.is_displayed())
        result.find_element_by_css_selector("a.description").click()
        WebDriverWait(self.browser, 2).until(
            EC.visibility_of(link)
        )
        self.assertTrue(link.is_displayed())

        link = result.find_element_by_class_name("google-book-page")
        self.assertIn("books.google.com/books?id=", link.get_attribute("href"))

    def test_user_searches_for_a_book_that_doesnt_exist(self):
        search = self.browser.find_element_by_id("id_query")
        search.send_keys(";oisejpaoin;dna;lsdqwa;lda;")
        search.submit()

        result = self.browser.find_element_by_css_selector(".error")
        self.assertIn("No books by that name were found!", result.text)
