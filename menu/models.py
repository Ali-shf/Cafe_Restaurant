from django.db import models
from authentication.models import *
from cloudinary.models import CloudinaryField
from authentication.models import CustomUser
from django.db.models import Avg

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    dish_id = models.IntegerField(default=0)
    quantity = models.IntegerField(blank=True)


    def __str__(self):
        return self.name
    
    @property
    def average_rating(self):
        return (
            Rating.objects
            .filter(item=self)
            .aggregate(avg=Avg('rating'))['avg']
            or 0
        )


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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    dish = models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.dish.name} - {self.user.username}"
    



class Stock(models.Model):
    sold_quantity = models.IntegerField(blank=True, default=0)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

    def __str__(self):
        return self.item.name
    
    @property
    def get_difference(self):
        total = self.item.quantity - self.sold_quantity
        return total
    



class Rating(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='ratings',
    )
    item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name='ratings',
    )
    rating = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'item')

    def __str__(self) -> str:
        return f'{self.item.name} rated {self.rating} by {self.user.username}'
