from django import forms
from pricesite import models

class RegistyForm(forms.Form):
    user_name = forms.CharField(label='Username', max_length=50)
    user_email = forms.EmailField(label='Email')


class LoginForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['Email',  'Password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['Email'].label = 'Email'
        self.fields['Password'].label = 'Password'

