from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import *
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    middle_name = forms.CharField(required=False)
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
        exclude=['email']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class PayslipUploadForm(forms.Form):
    payslip_file=forms.FileField(label='Upload Payslip PDF')