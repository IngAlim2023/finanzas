from django.db import models
from registration.models import User
from movimientos.models import Movimientos, Motivos
# Create your models here.


class Registros(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    movimiento = models.ForeignKey(Movimientos, on_delete=models.DO_NOTHING, null=True)
    motivos = models.ForeignKey(Motivos, on_delete=models.DO_NOTHING, null=True)
    descripcion = models.CharField(verbose_name='Descripción', max_length = 20)
    monto = models.DecimalField('Monto', max_digits=20, decimal_places=2)
    fecha = models.DateTimeField(verbose_name= 'Fecha', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Registro"
        verbose_name_plural = "Registros"

    def __str__(self) -> str:
        return f'{self.user} - {self.movimiento} - {self.motivos} - {self.monto}'