# administracion/forms.py

from django import forms
from usuarios.models import Usuario

class UsuarioAdminForm(forms.ModelForm):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Contraseña"
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'rol', 'is_active', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
