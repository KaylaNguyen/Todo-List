from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from lists.models import Item, List

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def new_list(request):
    new_list = List.objects.create()
    # list.save() doesn't get validated
    item = Item(text=request.POST['item_text'], list = new_list)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        new_list.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})
    return redirect('/lists/%d/' % (new_list.id))

def view_list(request, list_id):
    # to-do list
    list_ = List.objects.get(id = list_id)
    error = None
    # A list of all items in the to-do list
    # items = Item.objects.filter(list = list_)

    # Method == 'POST'
    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()

        except ValidationError:
            error = "You can't have an empty list item"

    # Method == 'GET'
    return render(
        request,
        'list.html',
        {'list': list_, 'error': error}
    )

def add_item(request, list_id):
    list_ = List.objects.get(id = list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id))

def delete_item(request, list_id, item_id):
    list_ = List.objects.get(id = list_id)
    item = Item.objects.get(id = item_id)
    item.delete()
    return redirect('/lists/%d/' % (list_.id))

def edit_list(request, list_id):
    list_ = List.objects.get(id=list_id)

    for item in list_.item_set.all():
        item.is_done = False
        item.save()

    item_ids = request.POST.getlist('mark_item_done')
    for item_id in item_ids:
        item = Item.objects.get(id=item_id)
        item.is_done = True
        item.save()

    return redirect('/lists/%d/' % (list_.id))
