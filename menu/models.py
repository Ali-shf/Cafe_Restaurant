from django.db import models
from authentication.models import *
from cloudinary.models import CloudinaryField


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    dish_id = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class MenuItemImage(models.Model):
    menu_item = models.ForeignKey(
        MenuItem,
        related_name='images',
        on_delete=models.CASCADE,
    )
    image = CloudinaryField('image')

    def __str__(self) -> str:
        return f'Image for {self.menu_item.name}'
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.dish.name} - {self.user.username}"
    

