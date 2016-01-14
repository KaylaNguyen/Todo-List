from django.core.urlresolvers import resolve
from django.utils.html import escape
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item, List

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)
        #
        # self.assertTrue(response.content.startswith(b'<html>'))
        # self.assertIn(b'<title>To-Do lists</title>', response.content)
        # self.assertTrue(response.content.strip().endswith(b'</html>'))

    # def test_home_page_doesnt_save_on_GET_request(self):
    #     request = HttpRequest()
    #     home_page(request)
    #     self.assertEqual(Item.objects.count(), 0)

class NewListTest(TestCase):
    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )

        ## equals to the post request above
        # request = HttpRequest()
        # request.method = 'POST'
        # request.POST['item_text'] = 'A new list item'
        # response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

        # check if the template is correct
        # self.assertIn('A new list item', response.content.decode())
        #
        # expected_html = render_to_string(
        #     'home.html', { 'new_item_text': 'A new list item'}
        # )
        # self.assertEqual(response.content.decode(), expected_html)

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data = {'item_text': 'A new list item'}
        )
        new_list = List.objects.first()

        # status code is 200: OK
        # status code 404: error
        # status code 302: it's somewhere else (go somewhere else to get that data)
        #     self.assertEqual(response.status_code, 302)
        #     self.assertEqual(response['location'], '/lists/the-only-list/')

        self.assertRedirects(response, '/lists/%d/' % (new_list.id))

    def test_validation_errors_are_sent_back_to_home_page(self):
        response = self.client.post('/lists/new', data = {'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_items_arent_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

# class NewItemTest(TestCase):

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        new_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (new_list.id))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_list(self):
        new_list = List.objects.create()
        Item.objects.create(text='itemey 1', list = new_list)
        Item.objects.create(text='itemey 2', list = new_list)
        other_list = List.objects.create()
        Item.objects.create(text='other item 1', list = other_list)
        Item.objects.create(text='other item 2', list = other_list)

        response = self.client.get('/lists/%d/' % (new_list.id))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other item 1')
        self.assertNotContains(response, 'other item 2')

    def test_can_save_a_POST_request_to_an_existing_list(self):
        correct_list = List.objects.create()

        # A slash is to retrieve data, no slash is to sending
        self.client.post(
            '/lists/%d/' % (correct_list.id),
            data = {'item_text': 'A new item for an existing list'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    # def test_redirects_to_list_view(self):
    #     correct_list = List.objects.create()
    #     response = self.client.post(
    #         '/lists/%d/' % (correct_list.id),
    #         data = {'item_text': 'A new item for an existing list'}
    #     )
    #     self.assertRedirects(response, '/lists/%d/' % (correct_list.id))

    def test_passes_correct_list_to_template(self):
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id))
        self.assertEqual(response.context['list'], correct_list)

    def validation_errors_stay_on_list_page(self):
        current_list = List.objects.create()
        response = self.client.post(
            '/lists/%d' % (current_list.id),
            data={'item_text': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape ("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_items_arent_saved(self):
        current_list = List.objects.create()
        self.client.post(
            '/lists/%d' % (current_list.id),
            data={'item_text': ''}
        )
        self.assertEqual(Item.objects.count(), 0)

    def test_list_view_displays_checkbox(self):
        current_list = List.objects.create()
        Item.objects.create(text="Item 1", list=current_list)
        Item.objects.create(text="Item 2", list=current_list)

        response = self.client.get('/lists/%d/' % (current_list.id))

        self.assertContains(response, 'input type="checkbox"')

    def test_POST_items_marked_done(self):
        # create list and items
        current_list = List.objects.create()
        item1 = Item.objects.create(text="Item 1", list=current_list)
        item2 = Item.objects.create(text="Item 2", list=current_list)

        # POST data
        response = self.client.post(
            '/lists/%d/items/' % (current_list.id),
            data={'mark_item_done': item1.id}
        )
        # including toggle item
        self.assertRedirects(response, '/lists/%d/' % (current_list.id))

        # check the item is updated
        item1 = Item.objects.get(id=item1.id)
        item2 = Item.objects.get(id=item2.id)
        self.assertTrue(item1.is_done)
        self.assertFalse(item2.is_done)

    def test_POST_multiple_items_done(self):
        current_list = List.objects.create()
        item1 = Item.objects.create(text="Item 1", list=current_list)
        item2 = Item.objects.create(text="Item 2", list=current_list)

        response = self.client.post(
            '/lists/%d/items/' % (current_list.id),
            data={'mark_item_done': [item1.id, item2.id]}
        )

        item1 = Item.objects.get(id=item1.id)
        item2 = Item.objects.get(id=item2.id)
        self.assertTrue(item1.is_done)
        self.assertTrue(item2.is_done)

    def test_POST_zero_items_done(self):
        current_list = List.objects.create()
        item1 = Item.objects.create(text="Item 1", list=current_list)
        item2 = Item.objects.create(text="Item 2", list=current_list)

        response = self.client.post(
            '/lists/%d/items/' % (current_list.id),
            data={}
        )

        item1 = Item.objects.get(id=item1.id)
        item2 = Item.objects.get(id=item2.id)
        self.assertFalse(item1.is_done)
        self.assertFalse(item2.is_done)

    def test_POST_items_toggles_done(self):
        # create list and items
        current_list = List.objects.create()
        item1 = Item.objects.create(
            text="Item 1",
            list=current_list,
            is_done=True
        )

        item2 = Item.objects.create(
            text="Item 2",
            list=current_list,
            is_done=False
        )

        # POST data
        response = self.client.post(
            '/lists/%d/items/' % (current_list.id),
            data={'mark_item_done': item2.id}
        )
        # including toggle item
        self.assertRedirects(response, '/lists/%d/' % (current_list.id))

        # check the item is updated
        item1 = Item.objects.get(id=item1.id)
        item2 = Item.objects.get(id=item2.id)
        self.assertFalse(item1.is_done)
        self.assertTrue(item2.is_done)
