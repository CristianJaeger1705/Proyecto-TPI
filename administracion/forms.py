# administracion/forms.py

from django import forms
from usuarios.models import Usuario
import re

class UsuarioAdminForm(forms.ModelForm):

    nombre = forms.CharField(
        max_length=30,
        required=True,
        label="Nombre",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    apellido = forms.CharField(
        max_length=30,
        required=True,
        label="Apellido",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'rol', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+$', nombre):
            raise forms.ValidationError("El nombre solo puede contener letras.")
        return nombre

    def clean_apellido(self):
        apellido = self.cleaned_data.get("apellido")
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+$', apellido):
            raise forms.ValidationError("El apellido solo puede contener letras.")
        return apellido
