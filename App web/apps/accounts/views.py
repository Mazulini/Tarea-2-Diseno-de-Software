from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Usuario, Cliente
from .forms import LoginForm, RegisterForm
from django.utils import timezone
from django.contrib.auth.hashers import make_password

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

#Admin

@require_rol('admin')
def ver_usuarios(request):
    return render(request, 'accounts/admin/ver_usuarios.html')

@require_rol('admin')
def admin_ver_paquetes(request):
    return render(request, 'accounts/admin/ver_paquetes.html')

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

#Conductor 

@require_rol('conductor')
def conductor_ver_rutas(request):
    return render(request, 'accounts/conductor/ver_rutas.html')

#Cliente 

@require_rol('cliente')
def cliente_ver_paquetes(request):
    return render(request, 'accounts/cliente/ver_paquetes.html')

@require_rol('cliente')
def cliente_enviar_paquete(request):
    return render(request, 'accounts/cliente/enviar_paquete.html')