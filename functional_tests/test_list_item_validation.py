from unittest import skip
from .base import TodoFunctionalTest

class ItemValidationTest(TodoFunctionalTest):
    @skip("Haven't implemented this")
    def test_cannot_add_empty_list_item(self):
        # Edith goes to the homepage, and accidentally tries
        # to submit an empty list item
        # she hits "Enter" on the empty input box

        # The homepage refreshes, and there is an error message
        # saying that list items cannot be blank

        # she tries again with some text for the item which now works

        # Perversely tries to enter a second blank item

        # she receives a similar warning on the list page

        # And she can correct it by filling some text in
        self.fail('Finish the test!')
