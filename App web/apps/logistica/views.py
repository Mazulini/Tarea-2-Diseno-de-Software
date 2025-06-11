from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import AsignarPaqueteRutaForm, AsignarRutaConductorForm
from .models import Paquete, EnvioPaquete, Envio, Cliente, Ruta, EstadoDeEntrega

@login_required
def lista_paquetes(request):
    paquetes = Paquete.objects.select_related('remitente__usuario', 'estado_entrega').all()
    envios_paquetes = EnvioPaquete.objects.prefetch_related('envio__ruta', 'envio__conductor__usuario').all()
    context = {
        'paquetes': paquetes,
        'envios_paquetes': envios_paquetes,
    }
    return render(request, 'logistica/lista_paquetes.html', context)

@login_required
def asignar_paquete_ruta(request):
    if request.method == 'POST':
        form = AsignarPaqueteRutaForm(request.POST)
        if form.is_valid():
            paquete = form.cleaned_data['paquete']
            ruta = form.cleaned_data['ruta']
            envio = Envio.objects.create(
                ruta=ruta,
                fecha_hora_inicio=timezone.now()
            )
            EnvioPaquete.objects.create(envio=envio, paquete=paquete)
            messages.success(request, 'Paquete asignado a la ruta.')
            return redirect('logistica:lista_paquetes')
    else:
        form = AsignarPaqueteRutaForm()
    return render(request, 'logistica/asignar_paquete_ruta.html', {'form': form})

@login_required
def asignar_ruta_conductor(request):
    if request.method == 'POST':
        form = AsignarRutaConductorForm(request.POST)
        if form.is_valid():
            envio = form.cleaned_data['envio']
            conductor = form.cleaned_data['conductor']
            envio.conductor = conductor
            envio.save()
            en_transito = EstadoDeEntrega.objects.get(nombre_estado='En tránsito')
            envios_paquetes = EnvioPaquete.objects.filter(envio=envio)
            for ep in envios_paquetes:
                ep.paquete.estado_entrega = en_transito
                ep.paquete.save()
            messages.success(request, 'Ruta asignada al conductor y paquetes en tránsito.')
            return redirect('logistica:lista_paquetes')
    else:
        form = AsignarRutaConductorForm()
    return render(request, 'logistica/asignar_ruta_conductor.html', {'form': form})