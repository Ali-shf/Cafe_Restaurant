from django.urls import path , include
from . import views


urlpatterns = [
    path('dish/adding/',views.adding_menu,name='adding_dish'),
    path('menu/list/',views.menu_list,name='menu_list'),
    path('menu/delete/<int:menu_id>/', views.delete_menu, name='delete_menu'),
    path("api/about/", views.AboutUsAPIView.as_view(), name="about_api"),
    path("api/admin/", include("ownerlogin.urls_admin")),
]
