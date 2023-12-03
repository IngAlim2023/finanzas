from django.shortcuts import render
from django import forms
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import *
# Create your views here.

#Vistas basadas en clases:
from django.views.generic.base import TemplateView

#conf repositorio Ede
from typing import Optional, Type
from django.forms.models import BaseModelForm
from django.shortcuts import render

# vistas basadas en clases:
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView

# Método decorador de login:
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# Formularios propios:
from .forms import SingUpUserFormWithEmail, ProfileUserForm

from django.urls import reverse_lazy
from django import forms

class SignUpUserView(CreateView):
    form_class= SingUpUserFormWithEmail
    template_name = 'registration/registro.html'

    def get_success_url(self):
        return reverse_lazy('tu_vista_login') + '?register' 

    def get_form(self, form_class= None):
        form = super(SignUpUserView, self).get_form()
        # Agregamos estilos al formulario a través de widgets:
        form.fields['username'].widget = forms.TextInput(attrs={'placeholder':'NickName', 'class':'form-control mb-2'})
        form.fields['email'].widget = forms.EmailInput(attrs={'placeholder':'email@mail.com', 'class':'form-control mb-2'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirma el Password'})

        return form
    

@method_decorator(login_required, name='dispatch')
class ProfileUserUpdate(UpdateView):
    form_class = ProfileUserForm
    success_url = reverse_lazy('inicio')
    template_name = 'registration/datosPersonales.html'

    # Métodos:
    def get_object(self):
        profile, created = User.objects.get_or_create(id = self.request.user.id) # QuerySet de usuario: Select * from user where id = request.user.id
        return profile

