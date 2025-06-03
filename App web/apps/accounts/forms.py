# apps/accounts/forms.py

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario', max_length=150)
    password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
