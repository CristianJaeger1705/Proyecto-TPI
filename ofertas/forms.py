from django import forms
from .models import OfertaLaboral

class Ofertasform(forms.ModelForm):
    class Meta:
        model = OfertaLaboral
<<<<<<< HEAD
        fields=['titulo','tipo_empleo','descripcion','salario','ubicacion','estado']
=======
        fields='__all__'
        exclude = ['empresa']
>>>>>>> e1022b1d198e8020d6d9f8dd9b8f53fb365017b2
        widgets = {
            'tipo_empleo': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'salario': forms.NumberInput(attrs={'class': 'form-control','step': '0.01','min': '0'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
<<<<<<< HEAD
     self.request=kwargs.pop('request',None)
     super().__init__(*args, **kwargs)
    
    def save(self,commit=True):
       instance=super().save(commit=False)
       if self.request and hasattr(self.request.user,'perfil_empresa'):
          instance.empresa=self.request.user.perfil_empresa
       if commit:
          instance.save()
       return instance
=======
     super().__init__(*args, **kwargs)
>>>>>>> e1022b1d198e8020d6d9f8dd9b8f53fb365017b2
