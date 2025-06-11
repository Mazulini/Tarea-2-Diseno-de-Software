from django import forms
from .models import Paquete, Envio, Conductor

#forms de login

class LoginForm(forms.Form):
    correo = forms.EmailField(label='Correo', max_length=150)
    contrasena = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

class RegisterForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=True)
    correo = forms.EmailField(max_length=150, required=True)
    contrasena = forms.CharField(widget=forms.PasswordInput, required=True)
    direccion = forms.CharField(max_length=300, required=True)
    telefono = forms.CharField(max_length=20, required=False)  # este puede ser opcional

#forms de logistica

class AsignarPaqueteEnvioForm(forms.Form):
    paquete = forms.ModelChoiceField(
        queryset=Paquete.objects.filter(estado_entrega=1),
        label='Paquete'
    )
    envio = forms.ModelChoiceField(
        queryset=Envio.objects.filter(fecha_hora_fin__isnull=True),
        label='Envío'
    )

class AsignarEnvioConductorForm(forms.Form):
    envio = forms.ModelChoiceField(
        queryset=Envio.objects.filter(conductor__isnull=True),
        label='Envío'
    )
    conductor = forms.ModelChoiceField(
        queryset=Conductor.objects.filter(envio__isnull=True),
        label='Conductor'
    )