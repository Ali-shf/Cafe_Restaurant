from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from authentication import *
from .models import *
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from .models import MenuItem 
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from .models import MenuItem, Stock, Rating
from menu.serializers import MenuItemSerializer, StockSerializer, RatingSerializer,SearchMenuItemSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.filters import SearchFilter

class SearchMenuItemViewSet(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = SearchMenuItemSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']

class MenuItemViewSet(ModelViewSet):
    queryset = (
    MenuItem.objects
    .annotate(average_rating=Avg('ratings__rating'))
    .prefetch_related('images')
)
    serializer_class = MenuItemSerializer
    parser_classes = [MultiPartParser, FormParser]

class RatingViewSet(ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.select_related('item')
    serializer_class = StockSerializer
    permission_classes = [IsAdminUser]


@login_required(login_url='/login/')
def menu(request):
    dishes = MenuItem.objects.all()
    cart_count = Cart.objects.filter(user=request.user, is_ordered=False).count()
    return render(request,'menu.html', {
        'dishes': dishes,
        'cart_count': cart_count
    })

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





def menu_detail(request, id):
    dish = get_object_or_404(MenuItem, id=id)
    return render(request, 'menu_detail.html', {
        'dish': dish
    })
