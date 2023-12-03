from django.db import models

# Create your models here.

class Departamento(models.Model):
    nombre_departamento = models.CharField('Departamento', max_length=25)
    codigo_departamento = models.CharField('Código departamento', max_length=2)
    latitud = models.FloatField('Latitud', blank=True, null=True)
    longitud = models.FloatField('Longitud', blank=True, null=True)
    

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
    
    def __str__(self) -> str:
        return f'{self.nombre_departamento} {self.codigo_departamento}'

class Ciudad(models.Model):
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    nombre_ciudad = models.CharField('Ciudad', max_length=25)
    codigo_ciudad = models.CharField('Código ciudad', max_length=2)
    latitud = models.FloatField('Latitud', blank=True, null=True)
    longitud = models.FloatField('Longitud', blank=True, null=True)
    

    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
    
    def __str__(self) -> str:
        return f'{self.nombre_ciudad} {self.codigo_ciudad}'