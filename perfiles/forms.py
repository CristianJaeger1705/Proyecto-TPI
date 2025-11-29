from django import forms
from .models import PerfilCandidato, PerfilEmpresa

class PerfilCandidatoForm(forms.ModelForm):
    class Meta:
        model = PerfilCandidato
        fields = ['profesion', 'habilidades', 'experiencia', 'departamento', 'cv_url', 'disponibilidad']
        widgets = {
            'habilidades': forms.Textarea(attrs={'rows': 3}),
            'experiencia': forms.Textarea(attrs={'rows': 3}),
        }

class PerfilEmpresaForm(forms.ModelForm):
    class Meta:
        model = PerfilEmpresa
        fields = [
            'nombre_empresa',
            'rubro',
            'descripcion',
            'sitio_web',
            'contacto',
            'logo'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

    # Validación opcional pero recomendada:
    def clean_nombre_empresa(self):
        nombre = self.cleaned_data.get('nombre_empresa')
        if not nombre:
            raise forms.ValidationError("El nombre de la empresa es obligatorio.")
        return nombre
