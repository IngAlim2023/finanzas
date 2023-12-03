from django.urls import path
from .views import *

urlpatterns = [
    #path('', views.index, name='index'),
    path('registro/', SignUpUserView.as_view(), name="registro"),
    path('datos/', ProfileUserUpdate.as_view(), name="datos"),
]