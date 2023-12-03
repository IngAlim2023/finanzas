from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SingUpUserFormWithEmail(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Requerido, asegurese de que sea un correo válido!')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El email ya está registrado, prueba con otro.")
        return email

class ProfileUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 
                'first_name',
                'last_name',
                'tipo_id',
                'identification',
                'photo',
                'city',
                'address',
                'phone',
                'birthday',
            ]
        labels = {
            'username':'Usuario',
            'first_name':'Primer nombre',
            'last_name':'Apellidos',
            'tipo_id':'Tipo de documento',
            'identification':'Número de identificación',
            'photo':'Foto',
            'city':'Ciudad',
            'address':'Dirección',
            'phone':'Teléfono',
            'birthday':'Fecha de nacimiento',
        }
        widgets = {
            'username':  forms.TextInput(attrs={'class': 'form-control'}),
            'first_name':  forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_id':  forms.Select(attrs={'class': 'form-select'}),
            'identification':  forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'city':  forms.Select(attrs={'class': 'form-select'}),
            'address':  forms.TextInput(attrs={'class': 'form-control'}),
            'phone':  forms.TextInput(attrs={'class': 'form-control'}),
            'birthday':  forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            
        }