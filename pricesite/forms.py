from django import forms
from pricesite import models


class LoginForm(forms.Form):
    name = forms.CharField(label="Username", max_length=20)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput, min_length=6, max_length=20)


class AuthenticationForm(forms.Form):
    name = forms.CharField(label="Username", max_length=20)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, min_length=6, max_length=20)
