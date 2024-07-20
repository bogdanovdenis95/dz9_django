# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')  # Убедитесь, что 'username' удален из полей

class PasswordResetForm(DjangoPasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254)
