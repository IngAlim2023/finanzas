from django.contrib import admin
from .models import TipoDocumento, User

# Register your models here.
admin.site.register(TipoDocumento)
admin.site.register(User)