from django import forms

class LoginForm(forms.Form):
    correo = forms.EmailField(label='Correo', max_length=150)
    contrasena = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
