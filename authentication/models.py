from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# from authentication.managers import CustomUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CustomUser(AbstractUser):
    # username = None
    email = models.EmailField(_("email address"), unique=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    phone_regex = RegexValidator(
        regex=r'^(\+98|0)?9\d{9}$',
        message='Phone must start with 09 like (09123456789) or +98 like (+989123456789).',
    )
    age = models.PositiveIntegerField(null=True, blank=True)
    birth_date = models.DateField()
    address = models.TextField(null=True, blank=True)
    gender = models.CharField(
        choices=GENDER_CHOICES, 
        blank=True, 
        null=True,
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=13,
        unique=True,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

    
    


    def __str__(self) -> str:
        return self.username

class AdminProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='admin_profile',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.user.username
    

    def is_staff(self):
        self.user.is_staff = True
        self.user.save()



class CustomerProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='customer_profile',
    )
    zip_code = models.CharField(max_length=10)
    loyalty_points = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.username
    
    