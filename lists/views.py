from django.shortcuts import render, redirect
from lists.models import Item, List

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def new_list(request):
    new_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list = new_list)
    return redirect('/lists/%d/' % (new_list.id))

def view_list(request, list_id):
    list_ = List.objects.get(id = list_id)
    items = Item.objects.filter(list = list_)
    return render(request, 'list.html', {'items': items,})
