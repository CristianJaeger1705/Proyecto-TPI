from django.shortcuts import redirect, render
from .models import OfertaLaboral
from ofertas.forms import Ofertasform
from django.core.paginator import Paginator
# Create your views here.
#Lista todos las vacantes disponibles

def ofertas_List(request):
    ofert = OfertaLaboral.objects.all().order_by('-fecha_publicacion')
    # Paginar - 10 registros por página
    paginator = Paginator(ofert, 10)
    # Obtener el número de página desde la URL
    page_number = request.GET.get('page')
    # Obtener la página actual
    ofertas = paginator.get_page(page_number)
    return render(request, 'ofertas/index.html',{'ofertas': ofertas })

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
