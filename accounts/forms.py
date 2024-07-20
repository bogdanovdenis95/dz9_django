
from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')


class PasswordResetForm(DjangoPasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254)
