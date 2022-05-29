from django import forms
from django.contrib.auth.models import User
from . import models


class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class ProfileForm(forms.ModelForm):
    phone_number = forms.IntegerField()
    class Meta:
        model=models.Profile
        fields=['phone_number']

class UserLoginForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['password']

class CommetProductForm(forms.ModelForm):
    class Meta:
        model = models.CommentProduct
        fields=['star', 'text']