from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/',views.user_login,name='login'),
    path('signup/successful/',views.success,name='success'),
    path('logout/',views.logoutuser,name='logout'),

]
