from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from registration.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.urls import reverse

#Modelos movimientos y motivos 
from movimientos.models import Movimientos, Motivos

from core.forms import RegistrarForm
#Para obener las finanzas de los usuarios:
from core.models import Registros
from django.db.models import Sum
#Vistas basadas en clases:
from django.views.generic.base import TemplateView

# Create your views here.

#Prueba Json
from django.http.response import JsonResponse
#Prueba grafico
from datetime import datetime

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
   
    #metodo para encontrar el 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.get_object()

        # Filtrar registros por el usuario y por movimiento de tipo Ingreso
        ingresos = Registros.objects.filter(user=usuario, movimiento__tipo_movimiento='Ingresos')

        # Calcular la suma del monto para los ingresos
        monto_total_ingresos = ingresos.aggregate(Sum('monto'))['monto__sum']

        context['monto_total_ingresos'] = monto_total_ingresos
        return context

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
            return redirect('registrar')  # Redirige a la vista de inicio después de un registro exitoso.

        return render(request, self.template_name, {'form': form})
    
@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener el usuario actualmente autenticado
        usuario = self.request.user

        # Filtrar registros por el usuario y por movimiento de tipo Ingreso o Egreso
        registros = Registros.objects.filter(user=usuario, movimiento__tipo_movimiento__in=['Ingresos', 'Egresos'])

        # Reversar el orden de los registros para mostrar el último primero
        

        # Calcular la suma del monto para los ingresos, egresos y disponible
        monto_total_ingresos = registros.filter(movimiento__tipo_movimiento='Ingresos').aggregate(Sum('monto'))['monto__sum'] or 0
        monto_total_egresos = registros.filter(movimiento__tipo_movimiento='Egresos').aggregate(Sum('monto'))['monto__sum'] or 0
        monto_total_disponible = monto_total_ingresos - monto_total_egresos

        

        context.update({
            'monto_total_ingresos': monto_total_ingresos,
            'monto_total_egresos': monto_total_egresos,
            'monto_total_disponible': monto_total_disponible,
            'registros' : registros[::-1],
        })

        return context

@method_decorator(login_required, name='dispatch')    
def delete(request, registro_id):
    registros = Registros.objects.filter(id=registro_id)
    registros.delete()
    return HttpResponseRedirect(reverse("inicio"))

@login_required
def update_view(request):
    registro_id = request.POST["id"]
    registro_movimiento_id = int(request.POST["movimiento"])
    registro_motivos_id = int(request.POST["motivos"])
    registro_descripcion = request.POST["descripcion"]
    registro_monto = request.POST["monto"]
    registro_fecha = request.POST["fecha"]

    # Obtener la instancia de Movimientos
    registro_movimiento = Movimientos.objects.get(pk=registro_movimiento_id)
    registro_motivo = Motivos.objects.get(pk=registro_motivos_id)
    # Actualizar el registro
    registro = Registros.objects.get(pk=registro_id)


    registro.movimiento = registro_movimiento
    registro.motivo = registro_motivos_id
    registro.descripcion = registro_descripcion
    registro.monto = registro_monto
    registro.fecha = registro_fecha
    
    #validadión del usuario:
    usuario_actual = request.user
        # Obtener el registro desde la base de datos
    registro_user = get_object_or_404(Registros, pk=registro_id)
    
    if registro_user.user != usuario_actual: 
        return HttpResponseRedirect(reverse('inicio'))
    else:
        registro.save()

    return HttpResponseRedirect(reverse('dashboard'))

@login_required
def update(request, registro_id):
    

    registro = Registros.objects.all()
    registro_unico = Registros.objects.get(pk=registro_id)
    
    #Validación para la vista(proteccion de datos):
    usuario_actual = request.user
    registro_user = get_object_or_404(Registros, pk=registro_id)
    
    #print(registro_unico)
    print(usuario_actual)
    print(registro_user.user)
    #print(registro_unico.movimiento)
    
    if registro_user.user != usuario_actual: 
        return HttpResponseRedirect(reverse('inicio'))
    else:
        
        context = {
        'registro': registro[::-1],
        'update': registro_unico,
        }

        return render(request, "core/actualizar.html", context)
    
#Prueba Json
@login_required
def basedatos (request):
    base_datos = list(Registros.objects.filter(user = request.user).values())
    data = {'base_datos': base_datos}
    return JsonResponse(data)

#Test Table:


def get_chart(request):
    ingresos = list(Registros.objects.filter(user=request.user, movimiento__tipo_movimiento='Ingresos').values_list('monto', flat=True))
   # egresos = list(Registros.objects.filter(user=request.user, movimiento__tipo_movimiento='Egresos').values_list('monto', flat=True))
    fechas = list(Registros.objects.filter(user=request.user, movimiento__tipo_movimiento='Ingresos').values_list('fecha', flat=True))
    fechas_formateadas = [fecha.strftime("%y-%m") if fecha else None for fecha in fechas]
    chart = {
        'title': {
            'text': "Ingresos"
        },
        'tooltip': {
            'trigger': 'axis',
            'axisPointer':{
                'type': 'cross',
                'label':{
                    'backgroundColor': '#6a7985'
                }
            },
        },
        'legend': {
            'data': ['Ingresos']
        },
        'toolbox': {
            'feature': {
                'saveAsImage': {}
            }
        },
        'grid': {
            'left': '3%',
            'right': '4%',
            'bottom': '3%',
            'containLabel': True
        },
        'xAxis': [
            {
                'type': 'category',
                'boundaryGap': False,
                'data': fechas_formateadas
            }
        ],
        'yAxis': [
            {
                'type': 'value'
            }
        ],
        'series': [
            {
                'name': 'Ingresos',
                'type': 'line',
                'stack': 'Total',
                'areaStyle': {
                    'color': '#80fd04'
                },
                'emphasis': {
                    'focus': 'series'
                },
                'data': ingresos,
            },
        ],
    }

    return JsonResponse(chart)

def get_chart_dos(request):
    egresos = list(Registros.objects.filter(user=request.user, movimiento__tipo_movimiento='Egresos').values_list('monto', flat=True))
   # egresos = list(Registros.objects.filter(user=request.user, movimiento__tipo_movimiento='Egresos').values_list('monto', flat=True))
    fechas = list(Registros.objects.filter(user=request.user, movimiento__tipo_movimiento='Egresos').values_list('fecha', flat=True))
    fechas_formateadas = [fecha.strftime("%y-%m") if fecha else None for fecha in fechas]
    chart = {
        'title': {
            'text': "Egresos"
        },
        'tooltip': {
            'trigger': 'axis',
            'axisPointer':{
                'type': 'cross',
                'label':{
                    'backgroundColor': '#6a7985'
                }
            },
        },
        'legend': {
            'data': ['Egresos']
        },
        'toolbox': {
            'feature': {
                'saveAsImage': {}
            }
        },
        'grid': {
            'left': '3%',
            'right': '4%',
            'bottom': '3%',
            'containLabel': True
        },
        'xAxis': [
            {
                'type': 'category',
                'boundaryGap': False,
                'data': fechas_formateadas
            }
        ],
        'yAxis': [
            {
                'type': 'value'
            }
        ],
        'series': [
            {
                'name': 'Egresos',
                'type': 'line',
                'stack': 'Total',
                'areaStyle': {
                    'color': '#d32626'
                },
                'emphasis': {
                    'focus': 'series'
                },
                'data': egresos,
            },
        ],
    }

    return JsonResponse(chart)