from django.shortcuts import redirect, render
from .models import OfertaLaboral
from ofertas.forms import Ofertasform

# Create your views here.
#Lista todos las vacantes disponibles
ofert = OfertaLaboral.objects.all()
def ofertas_List(request):
    return render(request, 'ofertas/index.html',{'ofertas': ofert })

#Funcion para agregar una nueva vacante
def agregar_Campos(request):
    formulario = Ofertasform(request.POST or None)
    if formulario.is_valid():
      formulario.save()
      return redirect('ofertas')
    return render(request, 'ofertas/create.html',{'formulario': formulario})


#Funcion para editar un dato
def editar_Campo(request,id):
    oferta=OfertaLaboral.objects.get(id=id)
    formulario=Ofertasform(request.POST or None,instance=oferta)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('ofertas')
    return render(request, 'ofertas/edit.html',{'formulario':formulario})
