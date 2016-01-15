from .base import TodoFunctionalTest

class ManyListTest(TodoFunctionalTest):
    def change_list_name(self, list_name):
        inputbox = self.browser.find_element_by_id('id_rename_list')
        inputbox.clear()
        inputbox.send_keys(list_name + '\n')

    def test_can_create_and_view_multiple_lists(self):
        # Edith comes to the home pade, creates a new list
        # and fills in her grocery list.
        self.browser.get(self.live_server_url)
        self.enter_a_new_item('Buy milk')
        self.enter_a_new_item('Buy cheese')
        self.check_for_row_in_list_table('Buy milk')
        self.check_for_row_in_list_table('Buy cheese')

        # She sees she can change a list name
        self.change_list_name('Groceries')

        # Edith goes back to the homepade, and sees her grocery list
        self.browser.get(self.live_server_url)
        self.check_for_row_in_list_table('Groceries')

        # Edith creates a new list for her Art History homework
        self.enter_a_new_item('Read Camille')

        # Edith opens the home page later & see both lists
        self.browser.get(self.live_server_url)
        self.check_for_row_in_list_table('Groceries')
        self.check_for_row_in_list_table('Read Camille')

        # Edith goes to the grocery list and sees what she needs to buy
        row = self.find_table_row('Groceries')
        row.find_element_by_tag_name('a').click()
        self.check_for_row_in_list_table('Buy milk')
        self.check_for_row_in_list_table('Buy cheese')
