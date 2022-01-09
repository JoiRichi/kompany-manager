from django import forms
from .models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='Kindly enter a valid email address')
    class Meta:
        model = CustomUser
        fields = ('email', )



class LoginForm(forms.Form):
    email= forms.CharField(max_length= 250,label="Enter username")
    password= forms.CharField(max_length= 30, label='Password', widget=forms.PasswordInput)