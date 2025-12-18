from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from authentication import *
from .models import *
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models import Sum


@login_required(login_url='/login/')
def menu(request):
    categories = Category.objects.all()

    selected_category_id = request.GET.get("category")
    if selected_category_id:
        dishes = MenuItem.objects.filter(category_id=selected_category_id)
    else:
        dishes = MenuItem.objects.all()

    cart_count = Cart.objects.filter(user=request.user, is_ordered=False).count()

    context = {
        "dishes": dishes,
        "categories": categories,
        "selected_category_id": int(selected_category_id) if selected_category_id else None,
        "cart_count": cart_count,
    }
    return render(request, "menu.html", context)

@login_required(login_url='/login/')
def add_to_cart(request, dish_id):
    dish = MenuItem.objects.get(id=dish_id)  
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        dish=dish,
        is_ordered=False
    )
    messages.success(request, f"{dish.name} has been added to your cart!")
    return redirect('menu')  


@login_required(login_url='/login/')
def acart(request):
    cart_items = Cart.objects.filter(user=request.user, is_ordered=False)
    total_cost = cart_items.aggregate(Sum('dish__price'))['dish__price__sum'] or 0
    total_cost = sum(item.dish.price for item in cart_items)
    gst = total_cost * Decimal('0.18')  
    total_with_gst = total_cost + gst
    context = {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'gst': gst,
        'total_with_gst': total_with_gst,
    }
    return render(request, 'cart.html', context)

@login_required(login_url='/login/')
def place_order(request):
    
    cart_items = Cart.objects.filter(user=request.user, is_ordered=False)

    
    for item in cart_items:
        item.is_ordered = True
        item.save()

    
    messages.success(request, "Your order has been placed successfully!")
    return redirect('menu')  


@login_required(login_url='/login/')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user, is_ordered=False)
    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required(login_url='/login/')
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart successfully.')
    return redirect('cart_item')



