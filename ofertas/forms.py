from datetime import date
from django import forms
from .models import OfertaLaboral

class Ofertasform(forms.ModelForm):
    class Meta:
        model = OfertaLaboral
        fields=['titulo','tipo_empleo','descripcion','salario','ubicacion','estado','fecha_expiracion']
        widgets = {
            'tipo_empleo': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'salario': forms.NumberInput(attrs={'class': 'form-control','step': '0.01','min': '0'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_expiracion': forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date','class': 'form-control','min': date.today().isoformat() }),}
    def __init__(self, *args, **kwargs):
     self.request=kwargs.pop('request',None)
     super().__init__(*args, **kwargs)
    
    def save(self,commit=True):
       instance=super().save(commit=False)
       if self.request and hasattr(self.request.user,'perfil_empresa'):
          instance.empresa=self.request.user.perfil_empresa
       if commit:
          instance.save()
       return instance
