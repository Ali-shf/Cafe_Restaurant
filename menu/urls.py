from django.urls import path
from . import views

urlpatterns = [
    path('menu/',views.menu,name='menu'),
    path('add-to-cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/',views.cart,name='cart_item'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),

    
    ]