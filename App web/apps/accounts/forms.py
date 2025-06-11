from django import forms

class LoginForm(forms.Form):
    correo = forms.EmailField(label='Correo', max_length=150)
    contrasena = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

class RegisterForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=True)
    correo = forms.EmailField(max_length=150, required=True)
    contrasena = forms.CharField(widget=forms.PasswordInput, required=True)
    direccion = forms.CharField(max_length=300, required=True)
    telefono = forms.CharField(max_length=20, required=False)  # este puede ser opcional
