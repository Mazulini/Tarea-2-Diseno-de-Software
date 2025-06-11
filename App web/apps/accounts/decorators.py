from django.shortcuts import redirect

def require_rol(rol_requerido):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if 'usuario_id' not in request.session:
                return redirect('login')
            if request.session.get('rol') != rol_requerido:
                return redirect('no_autorizado')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
