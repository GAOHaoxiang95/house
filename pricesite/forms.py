from django import forms
from pricesite import models


class LoginForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['email',  'name','password',]

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = 'Email'
        self.fields['password'].label = 'Password'
        self.fields['name'].label = 'Nickname'


class AuthenticationForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
