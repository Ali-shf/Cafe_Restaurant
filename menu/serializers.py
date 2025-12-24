# menu/serializers.py
from rest_framework import serializers
from .models import Dish  # یا MenuItem

class DishReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ["id", "name", "description", "price", "image", "is_available"]

class DishWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ["name", "description", "price", "image", "is_available"]

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value
