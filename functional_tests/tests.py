# selenium can load websites, click on buttons, load URLs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase

# start up a new server and a new database system everytime
class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def enter_a_new_item(self, todo_text):
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(todo_text)
        inputbox.send_keys(Keys.ENTER)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        self.enter_a_new_item('Buy peacock feathers')

        # When she hits enter, she is taken to a new URL
        # and now the page lists "1. Buy peacock feathers"
        # as an item in a to-do list
        edith_list_url = self.browser.current_url
        self.assertRegexpMatches(edith_list_url, '/lists.+')
        self.check_for_row_in_list_table('1. Buy peacock feathers')
        # self.assertTrue(
        #     any(row.text == '1: Buy peacock feathers' for row in rows),
        #     "New to-do item did not appear -- text was:\n%s" % (table.text),
        # )

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)
        self.enter_a_new_item('Use peacock feathers to make fly')

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1. Buy peacock feathers')
        self.check_for_row_in_list_table('2. Use peacock feathers to make fly')

        # Now a new user, Francis, comes along
        # We use a new browser session to make sure no info of Edith's come along
        # (EG cookies, localStorage)
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page. The is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new item
        # He is less interesting than Edith...
        self.enter_a_new_item('Buy milk')

        # Francis gets his own URL
        francis_list_url = self.browser.current_url
        self.assertRegexpMatches(francis_list_url, '/lists.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # There is still no trace of Edit's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, they both back to sleep
        # self.fail("Finish the app!")

    # def test_can_log_in_to_a_new_account(self):

    def test_layout_and_styling(self):
        # Edith goes to the homepage
        self.browser.set_window_size(1024, 768)
        self.browser.get(self.live_server_url)

        # She starts a new list and sees the box is centered
        self.check_imput_box_is_centered()

    def check_imput_box_is_centered(self):
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + (inputbox.size['width'] / 2),
            512,
            delta = 5
        )

if __name__ == '__main__':
    unittest.main()
