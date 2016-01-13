# selenium can load websites, click on buttons, load URLs
from unittest import skip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

# start up a new server and a new database system everytime
class TodoFunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def find_table_row(self, item_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        for row in rows:
            row_text = row.find_elements_by_tag_name('td')[2].text
            if item_text == row_text:
                return row
        return None


    def check_for_row_in_list_table(self, row_text):
        row = self.find_table_row(row_text)
        self.assertIsNotNone(row)

    def enter_a_new_item(self, todo_text):
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(todo_text)
        inputbox.send_keys(Keys.ENTER)
