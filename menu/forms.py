from django import forms
from .models import *

class DishForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = "__all__" 
