from django import forms

class RegistyForm(forms.Form):
    user_name = forms.CharField(label='Username', max_length=50)
    user_email = forms.EmailField(label='Email')