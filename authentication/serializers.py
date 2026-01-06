from authentication.models import (
    CustomUser,
    CustomerProfile,
    CustomUserManager,
)
from menu.serializers import RatingSerializer
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class RegistrationModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = CustomerProfile
        fields = [
            'id',
            'username',
            'email',
            'last_name',
            'password',
            'conform_password',
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match.'}
            )
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomerProfile.objects.create(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user


class CustomerProfileSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True, read_only=True)
    class Meta:
        model = CustomerProfile
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'ratings',
            'is_active',
            'is_staff',
            'date_joined',
            'last_login',
        ]
        read_only_fields = ['id', 'username', 'is_staff', 'date_joined']




class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = [
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
        ]
        extra_kwargs = {
            'is_staff': {'required': False},
            'is_active': {'required': False},
        }