from django.urls import path
from core.views import *
from . import views 
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', IndexPageView.as_view(), name= 'inicio'),
    path('registros/', RegistrarView.as_view(),  name= 'registrar'),
    path('dashboard/', DashboardView.as_view(),  name= 'dashboard'),
    #path('servicios/', Servicios.as_view(),  name= 'servicios'),
    #path('contacto/', Contacto.as_view(),  name= 'contacto'),
    path('login/', TuVistaLogin.as_view(), name='tu_vista_login'),
    path('perfilUsuario/<int:user_id>/', views.PerfilUsuario.as_view(), name='perfilUsuario'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]