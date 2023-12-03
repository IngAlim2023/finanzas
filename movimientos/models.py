from django.db import models

# Create your models here.
class Movimientos (models.Model):
    tipo_movimiento = models.CharField('Tipo de movimiento', max_length=10)
    created = models.DateField(auto_now_add=True)
    update = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Tipo de movimiento'
        verbose_name_plural = 'Tipos de movimientos'
    
    def __str__(self) -> str:
        return f'{self.tipo_movimiento}'

class Motivos (models.Model):
    tipo_motivo = models.CharField('Tipo de motivo', max_length=10)
    created = models.DateField(auto_now_add=True)
    update = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Tipo de motivo'
        verbose_name_plural = 'Tipos de motivos'
    
    def __str__(self) -> str:
        return f'{self.tipo_motivo}'