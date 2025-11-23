from django import forms
from .models import OfertaLaboral

class Ofertasform(forms.ModelForm):
    class Meta:
        model = OfertaLaboral
        fields='__all__'
        widgets = {
            'tipo_empleo': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'empresa': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'salario': forms.NumberInput(attrs={'class': 'form-control','step': '0.01','min': '0'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
     super().__init__(*args, **kwargs)