from django import forms
from .models import Paquete, Ruta, Envio, Conductor

class AsignarPaqueteRutaForm(forms.Form):
    paquete = forms.ModelChoiceField(
        queryset=Paquete.objects.filter(estado_entrega__nombre_estado='En Preparacion'),
        label='Paquete'
    )
    ruta = forms.ModelChoiceField(
        queryset=Ruta.objects.all(),
        label='Ruta'
    )

class AsignarRutaConductorForm(forms.Form):
    envio = forms.ModelChoiceField(
        queryset=Envio.objects.filter(conductor__isnull=True),
        label='Envío'
    )
    conductor = forms.ModelChoiceField(
        queryset=Conductor.objects.all(),
        label='Conductor'
    )