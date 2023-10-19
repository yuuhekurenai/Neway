from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Product


class LoginForm(AuthenticationForm):
    pass


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['color']
