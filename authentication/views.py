from django.shortcuts import render,redirect
from django.utils import timezone
from datetime import timedelta
from .models import *
from menu.urls import *
from .models import CustomUser 
from rest_framework.views import APIView
from authentication.serializers import (
    RegistrationModelSerializer,
    CustomerProfileSerializer,
    UpdateUserSerializer,
)
from rest_framework_simplejwt.tokens import (
    RefreshToken,
    # BlacklistedToken,
    # OutstandingToken,
)
from rest_framework import status, generics, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema




class RegisterUserViewSet(viewsets.ModelViewSet):
    permission_classes = RegistrationModelSerializer
    def create(self, request, *args, **kwargs):
        pass