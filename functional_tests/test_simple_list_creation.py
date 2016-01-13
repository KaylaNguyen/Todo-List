from unittest import skip
from selenium import webdriver
from .base import TodoFunctionalTest

class NewVisitorTest(TodoFunctionalTest):
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
        self.check_for_row_in_list_table('Buy peacock feathers')
        # self.assertTrue(
        #     any(row.text == '1: Buy peacock feathers' for row in rows),
        #     "New to-do item did not appear -- text was:\n%s" % (table.text),
        # )

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)
        self.enter_a_new_item('Use peacock feathers to make fly')

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('Buy peacock feathers')
        self.check_for_row_in_list_table('Use peacock feathers to make fly')

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
