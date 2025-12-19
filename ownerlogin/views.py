from django.shortcuts import render,redirect
from menu.models import *
from .forms import *
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def menu_list(request):
    menu_items = MenuItem.objects.all()  
    return render(request, 'menu_list.html', {'menu_items': menu_items})
@login_required(login_url='/login/')
def adding_menu(request):
    if request.method == "POST":
        dish_form = MenuItem_form(request.POST, request.FILES)
        if dish_form.is_valid():  
            dish_form.save()  
            return redirect('menu_list')  
    else:
        dish_form = MenuItem_form()  

    context = {"dish_form": dish_form}
    return render(request, 'addingmenu.html', context)

@login_required(login_url='/login/')
def delete_menu(request, menu_id):
    menu_item = get_object_or_404(MenuItem, id=menu_id)
    if request.method == "POST":
        menu_item.delete()  
        return redirect('menu_list') 
    return render(request, 'menu_list.html')