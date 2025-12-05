# mensajeria/forms.py
from django import forms
from .models import Chat
from usuarios.models import Usuario

class GrupoForm(forms.ModelForm):
    participantes = forms.ModelMultipleChoiceField(
        queryset=Usuario.objects.none(),  # inicial vacío, se actualizará en la vista
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Chat
        fields = ['nombre', 'participantes']
