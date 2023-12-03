from django import forms
from core.models import Registros


class RegistrarForm(forms.ModelForm):
    class Meta:
        model = Registros
        fields = [
                'movimiento',
                'motivos',
                'descripcion',
                'monto',
                'fecha',
                ]
        labels = {
            'movimiento':'Movimiento',
            'motivos':'Motivo',
            'descripcion':'Descripción',
            'monto':'Monto',
            'fecha':'Fecha',
        }
        widgets ={
            'movimiento': forms.Select(attrs={'class': 'form-select'}),
            'motivos':forms.Select(attrs={'class': 'form-select'}),
            'descripcion':forms.TextInput(attrs={'class': 'form-control'}),
            'monto':forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha':forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }