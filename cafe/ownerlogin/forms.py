from django import forms
from menu.models import MenuItem

class MenuItem_form(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'
        
