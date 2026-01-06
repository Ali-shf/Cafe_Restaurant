from django.shortcuts import render,redirect
from django.utils import timezone
from datetime import timedelta
from .models import *
from django.contrib.auth import authenticate,login,logout
from menu.urls import *
from django.shortcuts import render, redirect
from .models import CustomUser 
from .urls import *
from menu.views import *
from django.contrib import messages
from authentication.serializers import (
    RegistrationModelSerializer,
    CustomerProfileSerializer,
    UpdateUserSerializer,
)
from rest_framework_simplejwt.tokens import (
    RefreshToken,
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework import status, generics, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema


# --------------------------------------------------------------------
# Registration
# --------------------------------------------------------------------

class RegisterUserView(generics.CreateAPIView):
    serializer_class = RegistrationModelSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return CustomerProfile.objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        self.response = Response(
            {
                'message': 'User registered successfully.',
                'user': CustomerProfileSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )

        # Set cookies
        self.response.set_cookie(
            key='access_token',
            value=str(refresh.access_token),
            httponly=True,
            secure=False,
            expires=timezone.now() + timedelta(minutes=30),
            samesite='Lax',
        )
        self.response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=False,
            expires=timezone.now() + timedelta(days=7),
            samesite='Lax',
        )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return getattr(self, 'response', response)


# --------------------------------------------------------------------
# Login
# --------------------------------------------------------------------
@extend_schema(auth=None)
class LoginUserView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Username and password required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.check_password(password):
            return Response(
                {'error': 'Invalid credentials.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        response = Response(
            {
                'message': 'Login successful.',
                'user': CustomerProfileSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
            key='access_token',
            value=str(refresh.access_token),
            httponly=True,
            secure=False,
            expires=timezone.now() + timedelta(minutes=30),
            samesite='Lax',
        )
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=False,
            expires=timezone.now() + timedelta(days=7),
            samesite='Lax',
        )

        return response




# --------------------------------------------------------------------
# Logout
# --------------------------------------------------------------------
class LogoutUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user=request.user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)

        response = Response(
            {'message': 'Logged out successfully.'},
            status=status.HTTP_200_OK,
        )
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response

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
        user_check = CustomUser.objects.filter(username=username)
        if user_check.exists():
            context["error"] = "Username already exists."
            return render(request, "signup.html", context)

        

        # Create the user
        new_user = CustomUser(
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