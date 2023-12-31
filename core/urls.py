from django.urls import path
from core.views import *
from . import views 
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', IndexPageView.as_view(), name= 'inicio'),
    path('registros/', RegistrarView.as_view(),  name= 'registrar'),
    path('dashboard/', DashboardView.as_view(),  name= 'dashboard'),
    path('delete/<int:registro_id>', views.delete,  name= 'delete'),
    path('update', views.update_view, name='update_view'),
    path('update/<int:registro_id>', views.update,  name= 'update'),
    path('login/', TuVistaLogin.as_view(), name='tu_vista_login'),
    path('perfilUsuario/<int:user_id>/', views.PerfilUsuario.as_view(), name='perfilUsuario'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    #Prueba Json:
    path('datos/', views.basedatos, name = "basedatos"),

    #test Table

    path('get_chart/', views.get_chart, name = "get_chart"),
    path('get_chart_dos/', views.get_chart_dos, name = "get_chart_dos"),
    path('get_chart_tres/', views.get_chart_tres, name = "get_chart_tres"),
    path('get_chart_cuatro/', views.get_chart_cuatro, name = "get_chart_cuatro"),
]