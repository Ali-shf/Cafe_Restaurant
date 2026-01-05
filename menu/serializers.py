from rest_framework import serializers
from menu.models import (
    MenuItem, 
    MenuItemImage, 
    Stock,
    Rating,
)

from authentication.models import CustomUser



class MenuItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemImage
        fields = ['id', 'image']
    

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'rating', 'item']
        read_only_fields = ['id']

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value






class UserSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'ratings',
        ]


class MenuItemSerializer(serializers.ModelSerializer):
    images = MenuItemImageSerializer(many=True, read_only=True)
    average_rating = serializers.ReadOnlyField()
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = MenuItem
        fields = [
            "id",
            "name",
            "description",
            "price",
            "dish_id",
            "images",
            "uploaded_images",
            "average_rating",
        ]       


    def create(self, validated_data):
        images = validated_data.pop("uploaded_images", [])
        menu_item = MenuItem.objects.create(**validated_data)

        for img in images:
            MenuItemImage.objects.create(
                menu_item=menu_item,
                image=img
            )

        return menu_item





class StockSerializer(serializers.ModelSerializer):
    available_quantity = serializers.ReadOnlyField()
    class Meta:
        model = Stock
        fields = [
            'id',
            'item',
            'sold_quantity',
            'available_quantity',
        ]




