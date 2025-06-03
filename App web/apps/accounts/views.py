# apps/accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('/')  # Redirige al inicio o dashboard
            else:
                form.add_error(None, "Usuario o contraseña incorrectos.")

    return render(request, 'accounts/login.html', {'form': form})

