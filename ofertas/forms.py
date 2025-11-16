from django import forms
from .models import OfertaLaboral

class Ofertasform(forms.ModelForm):
    class Meta:
        model = OfertaLaboral
        fields='__all__'