from django.urls import path
from . import views


urlpatterns = [
    path('dish/adding/',views.adding_menu,name='adding_dish'),
    path('menu/list/',views.menu_list,name='menu_list'),
    path('menu/delete/<int:menu_id>/', views.delete_menu, name='delete_menu'),
]