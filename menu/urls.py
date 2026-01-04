from django.urls import path, include
from . import views
from rest_framework import routers
from menu.views import StockViewSet, MenuItemViewSet, RatingViewSet, SearchMenuItemViewSet

router = routers.DefaultRouter()
router.register(r'stock', StockViewSet, basename='stock')
router.register(r'menu-item', MenuItemViewSet, basename='menu-item')
router.register(r'ratings', RatingViewSet, basename='ratings')
router.register(r'search', SearchMenuItemViewSet,basename='search')

urlpatterns = [

    # HTML views
    path('menu/',views.menu,name='menu'),
    path('add-to-cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/',views.cart,name='cart_item'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('menu/<int:id>/', views.menu_detail, name='menu_detail'),

    # DRF
    path('api/', include(router.urls)),
]


