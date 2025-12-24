from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/',views.user_login,name='login'),
    path('signup/successful/',views.success,name='success'),
    path('logout/',views.logoutuser,name='logout'),
    path("api/", include("menu.api_urls")),


]
