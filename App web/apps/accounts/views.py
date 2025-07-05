from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Usuario, Cliente, Conductor, Paquete, EnvioPaquete, Envio, EstadoDeEntrega
from .forms import LoginForm, RegisterForm, AsignarPaqueteEnvioForm, AsignarEnvioConductorForm, ConductorVerEnvioForm
from django.utils import timezone
from django.contrib.auth.hashers import make_password

#Views de accounts

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']
            nombre = form.cleaned_data['nombre']
            direccion = form.cleaned_data['direccion']
            telefono = form.cleaned_data['telefono']

            if Usuario.objects.filter(correo=correo).exists():
                messages.error(request, 'Ya existe una cuenta con este correo')
            else:
                usuario = Usuario.objects.create(
                    correo=correo,
                    contrasena=make_password(contrasena),
                    nombre=nombre,
                    telefono=telefono,
                    fecha_registro=timezone.now(),
                    rol='cliente'
                )

                Cliente.objects.create(
                    usuario=usuario,
                    direccion=direccion
                )

                messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
                return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']

            try:
                usuario = Usuario.objects.get(correo=correo)
                if check_password(contrasena, usuario.contrasena):
                    request.session['usuario_id'] = usuario.id
                    request.session['rol'] = usuario.rol

                    if usuario.rol == 'admin':
                        return redirect('admin_dashboard')
                    elif usuario.rol == 'cliente':
                        return redirect('cliente_dashboard')
                    elif usuario.rol == 'conductor':
                        return redirect('conductor_dashboard')
                    else:
                        messages.error(request, 'Rol no reconocido')
                else:
                    messages.error(request, 'Contraseña incorrecta')
            except Usuario.DoesNotExist:
                messages.error(request, 'Correo no encontrado')
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {'form': form})

# Logout
def logout_view(request):
    request.session.flush()
    return redirect('login')

# No autorizado
def no_autorizado(request):
    # Aquí también asumo que el template está en una carpeta general templates/no_autorizado.html,
    # si está en accounts, cambiar a 'accounts/no_autorizado.html'
    return render(request, 'accounts/no_autorizado.html', status=403)

# Dashboards
def admin_dashboard(request):
    return render(request, 'accounts/admin/admin_dashboard.html')

def cliente_dashboard(request):
    return render(request, 'accounts/cliente/cliente_dashboard.html')

def conductor_dashboard(request):
    return render(request, 'accounts/conductor/conductor_dashboard.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

def es_admin(user):
    return user.is_authenticated and user.rol == 'admin'

from django.shortcuts import render
from .decorators import require_rol

#Views de logistica

#Admin

@require_rol('admin')
def ver_usuarios(request):
    return render(request, 'accounts/admin/ver_usuarios.html')

@require_rol('admin')
def admin_ver_paquetes(request):
    paquetes = Paquete.objects.select_related('remitente__usuario', 'estado_entrega').all()
    envios_paquetes = EnvioPaquete.objects.prefetch_related('envio__ruta', 'envio__conductor__usuario').all()
    context = {
        'paquetes': paquetes,
        'envios_paquetes': envios_paquetes,
    }
    return render(request, 'accounts/admin/ver_paquetes.html', context)

@require_rol('admin')
def ver_historial_envios(request):
    return render(request, 'accounts/admin/ver_historial_envios.html')

@require_rol('admin')
def registrar_socio(request):
    return render(request, 'accounts/admin/registrar_socio.html')

@require_rol('admin')
def gestionar_horarios(request):
    return render(request, 'accounts/admin/gestionar_horarios.html')

@require_rol('admin')
def admin_ver_rutas(request):
    return render(request, 'accounts/admin/ver_rutas.html')

@require_rol('admin')
def asignar_paquete_envio(request):
    if request.method == 'POST':
        form = AsignarPaqueteEnvioForm(request.POST)
        if form.is_valid():
            paquete = form.cleaned_data['paquete']
            paquete_id = paquete.id
            envio = form.cleaned_data['envio']
            envio_id = envio.id
            messages.success(request, 'Paquete asignado al envio.')
    else:
        form = AsignarPaqueteEnvioForm()
    return render(request, 'accounts/admin/asignar_paquete_envio.html', {'form': form})

@require_rol('admin')
def asignar_envio_conductor(request):
    if request.method == 'POST':
        form = AsignarEnvioConductorForm(request.POST)
        if form.is_valid():
            envio = form.cleaned_data['envio']
            envio_id = envio.id
            conductor = form.cleaned_data['conductor']
            conductor_id = conductor.id
            envio.conductor = conductor
            envio.save()
            en_transito = EstadoDeEntrega.objects.get(nombre_estado='En tránsito')
            envios_paquetes = EnvioPaquete.objects.filter(envio=envio)
            for ep in envios_paquetes:
                ep.paquete.estado_entrega = en_transito
                ep.paquete.save()
            messages.success(request, 'Envio asignado al conductor y paquetes en tránsito.')
            return redirect('admin_ver_paquetes')
    else:
        form = AsignarEnvioConductorForm()
    return render(request, 'accounts/admin/asignar_envio_conductor.html', {'form': form})

#Conductor 

@require_rol('conductor')
def conductor_ver_envios(request):
    usuario_id = request.session.get('usuario_id')
    conductor = Conductor.objects.get(usuario_id=usuario_id)
    envio_seleccionado = None

    if request.method == 'POST':
        form = ConductorVerEnvioForm(request.POST, conductor=conductor)
        if form.is_valid():
            envio_seleccionado = form.cleaned_data['envio']
    else:
        form = ConductorVerEnvioForm(conductor=conductor)

    return render(request,
                  'accounts/conductor/ver_envios.html',
                    {'form': form, 'envio_seleccionado': envio_seleccionado})

@require_rol('conductor')
def conductor_ver_paquetes_envio(request, envio_id):
    usuario_id = request.session.get('usuario_id')
    conductor = get_object_or_404(Conductor, usuario_id=usuario_id)
    envio = get_object_or_404(Envio, id=envio_id, conductor=conductor)

    paquetes = Paquete.objects.filter(enviopaquete__envio=envio)

    return render(request,
                  'accounts/conductor/ver_paquetes_envio.html',
                  {'envio': envio, 'paquetes': paquetes})

#Cliente 

@require_rol('cliente')
def cliente_ver_paquetes(request):
    return render(request, 'accounts/cliente/ver_paquetes.html')

@require_rol('cliente')
def cliente_enviar_paquete(request):
    usuario_id = request.session.get('usuario_id')
    cliente = get_object_or_404(Cliente, usuario_id=usuario_id)

    destinatarios = Cliente.objects.exclude(usuario_id=usuario_id)

    if request.method == 'POST':
        tipo = request.POST['tipo']
        contenido = request.POST['contenido']
        peso = request.POST['peso']
        dimensiones = request.POST['dimensiones']
        destinatario_id = request.POST['destinatario']

        estado_inicial = EstadoDeEntrega.objects.get(nombre_estado__istartswith='En prep')
        destinatario = get_object_or_404(Cliente, usuario_id=destinatario_id)

        Paquete.objects.create(
            remitente=cliente,
            tipo=tipo,
            contenido=contenido,
            peso=peso,
            dimensiones=dimensiones,
            destinatario=destinatario,
            estado_entrega=estado_inicial
        )

        messages.success(request, 'Paquete enviado correctamente.')
        return redirect('cliente_ver_paquetes')

    return render(request, 'accounts/cliente/enviar_paquete.html', {
        'destinatarios': destinatarios
    })