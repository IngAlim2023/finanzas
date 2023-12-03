from django.db import models
from django.contrib.auth.models import AbstractUser
# Importamos la libreria de texto enriquecido:
from ckeditor.fields import RichTextField
# Para la actualización de datos de usuario:
from django.dispatch import receiver
from django.db.models.signals import post_save
from localizacion.models import Ciudad, Departamento

# # funcion para la carga de imagenes de usuario:
def upload_image(instance, filename):
    return "img/users/{id}/{filename}".format( id = instance.pk, filename = filename)

class TipoDocumento(models.Model):
    tipo_documento = models.CharField('Tipo de documento', max_length=30)
    created = models.DateField(auto_now_add=True)
    update = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Tipo de documento'
        verbose_name_plural = 'Tipos de documentos'
    
    def __str__(self):
        return f'{self.tipo_documento}'

# Create your models here.
class User(AbstractUser):

    # Sobreescribo el campo'username':
    email = models.EmailField(verbose_name='Correo Electrónico', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    tipo_id = models.ForeignKey(TipoDocumento, on_delete=models.DO_NOTHING, null=True)
    identification = models.CharField(verbose_name='Número de Identificación', max_length = 20)
    photo = models.ImageField(verbose_name='Foto de Perfil', upload_to=upload_image, null=True, blank=True)
    city = models.ForeignKey(Ciudad, on_delete=models.DO_NOTHING, null=True)
    address = models.CharField(verbose_name= 'Dirección', max_length=255)
    phone = models.CharField(verbose_name= 'Telefono', max_length=255)
    birthday = models.DateField(verbose_name= 'Fecha de Nacimiento', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)



# Metodo de datos Seguros de Usuario:
@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        User.objects.get_or_create(id = instance.id) # Traiga el dato del usuario con id = request.user.id