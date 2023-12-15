from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import *
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    middle_name = forms.CharField()
    ippis_no=forms.NumberInput()
    file_no=forms.NumberInput()
    phone_no=forms.NumberInput()
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
