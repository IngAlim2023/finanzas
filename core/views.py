from typing import Any
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from django.utils.decorators import method_decorator
from registration.models import User
from django.contrib.auth import authenticate, login
from django.views import View
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.urls import reverse

from core.forms import RegistrarForm

#Vistas basadas en clases:
from django.views.generic.base import TemplateView

# Create your views here.

class IndexPageView(TemplateView):
    #Indicar que template usa esta vista
    template_name = 'core/index.html'
#def index (request):
#    return render(request, 'index.html')

class TuVistaLogin(TemplateView):
    template_name = 'registration/login.html'

    def post(self, request):
        if request.method == 'POST':
        # Procesar el formulario de inicio de sesión
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('inicio'))
            # Redirigir a la página deseada después del inicio de sesión exitoso
            else:
            # Manejar el caso de inicio de sesión fallido        
                return render(request, self.template_name, {'error_message': 'Nombre de usuario o contraseña incorrectos'})
            
    def get(self, request):
        return render(request, self.template_name)

@method_decorator(login_required, name='dispatch')
class PerfilUsuario(DetailView):
    model = User # Modelo que contiene la información del usuario
    template_name = 'registration/perfilUsuario.html'
    context_object_name = 'usuario'
    pk_url_kwarg = 'user_id'  # Esto le dice a Django que use 'user_id' en lugar de 'pk' en la URL

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('user_id')
        # Cambiar 'user_id' a 'pk' para que coincida con la URL
        return User.objects.filter(pk=user_id).first()

@method_decorator(login_required, name='dispatch')
class RegistrarView(CreateView):
    form_class = RegistrarForm
    template_name = 'core/registrar.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.user = self.request.user  # Asigna el usuario actual al registro
            registro.save()
            return redirect('inicio')  # Redirige a la vista de inicio después de un registro exitoso.

        return render(request, self.template_name, {'form': form})