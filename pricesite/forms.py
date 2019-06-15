from django import forms
from pricesite import models


class LoginForm(forms.Form):
    name = forms.CharField(label="Username", initial="Tourist")
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class AuthenticationForm(forms.Form):
    name = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
