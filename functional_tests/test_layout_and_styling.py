from .base import TodoFunctionalTest

class LayoutAndStyling(TodoFunctionalTest):
    def test_layout_and_styling(self):
        # Edith goes to the homepage
        self.browser.set_window_size(1024, 768)
        self.browser.get(self.live_server_url)

        # She starts a new list and sees the box is centered
        self.check_input_box_is_centered()

    def check_input_box_is_centered(self):
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + (inputbox.size['width'] / 2),
            512,
            delta = 5
        )
