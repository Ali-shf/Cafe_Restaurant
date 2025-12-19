from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate,login,logout
from menu.urls import *
from django.shortcuts import render, redirect
from .models import User 
from .urls import *
from menu.views import *
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request,'home.html')

def user_login(request):
    if request.user.is_authenticated:
        # Redirect based on the user role once they are already authenticated
        if request.user.username.startswith("emp") and request.user.username[3:].isdigit():
            return redirect('menu_list')  # Employee menu
        else:
            return redirect('menu')  # Customer menu

    context = {"error": ""}

    if request.method == 'POST':
        # Authenticate the user with provided credentials
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is not None:  # If the user is successfully authenticated
            login(request, user)

            # Role-based redirection logic
            if user.username.startswith("emp") and user.username[3:].isdigit():
                return redirect('menu_list')  # Employee menu
            else:
                return redirect('menu')  # Customer menu
        else:
            # Authentication failed, show an error message
            context['error'] = 'Invalid username or password'
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html', context)

def signup(request):
    context = {"error": ""}
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        dob = request.POST.get('DOB')
        address = request.POST.get('address')
        age = request.POST.get('age')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validation
        user_check = User.objects.filter(username=username)
        if user_check.exists():
            context["error"] = "Username already exists."
            return render(request, "signup.html", context)

        

        # Create the user
        new_user = User(
            username=username,
            first_name=firstname,
            last_name=lastname,
            email=email,
            dob=dob,
            address=address,
            age=age
        )
        new_user.set_password(password)
        new_user.save()
        messages.success(request, "Registration successful! Please log in to continue.")
        return redirect('login')  

    return render(request, 'signup.html', context)

def success(request):
    return render(request, 'success_page.html')

def logoutuser(request):
    Cart.objects.filter(user=request.user, is_ordered=False).delete()
    logout(request)
    return redirect('/')    