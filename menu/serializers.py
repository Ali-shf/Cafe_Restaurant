from rest_framework import serializers
from menu.models import MenuItem, MenuItemImage



class MenuItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemImage
        fields = ['id', 'image']
    



class MenuItemSerializer(serializers.ModelSerializer):
    images = MenuItemImageSerializer(many=True, read_only=True)
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
