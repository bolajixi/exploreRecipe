from django import forms
from django.forms import TextInput
from .models import Ingredient


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('name',)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your ingredient here'}),
        }
