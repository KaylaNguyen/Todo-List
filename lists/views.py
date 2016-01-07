from django.shortcuts import render, redirect
from lists.models import Item, List

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def new_list(request):
    new_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list = new_list)
    return redirect('/lists/the-only-list/')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items,})
