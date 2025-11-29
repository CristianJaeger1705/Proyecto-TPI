from django.contrib import messages
from ofertas.utils import es_empresa

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import OfertaLaboral
from ofertas.forms import Ofertasform
from django.core.paginator import Paginator
from ofertas.utils import es_empresa
from django.contrib.auth.decorators import login_required


def listado_ofertas(request):
    # Solo mostrar ofertas activas
    ofertas = OfertaLaboral.objects.filter(estado='activa').order_by('-fecha_publicacion')
    return render(request, 'ofertas/listado_ofertas.html', {'ofertas': ofertas})


def detalle_oferta(request, oferta_id):
    oferta = get_object_or_404(OfertaLaboral, id=oferta_id, estado='activa')
    return render(request, 'ofertas/detalle_oferta.html', {'oferta': oferta})
# =====================================================
# LISTAR OFERTAS - EMPRESA ve las suyas / CANDIDATOS ven todas
# =====================================================
@login_required(login_url='login')
def ofertas_List(request):

    usuario = request.user

    # ---------------------------------------------
    # SI ES EMPRESA
    # ---------------------------------------------
    if es_empresa(usuario):

        try:
            empresa = usuario.perfilempresa
        except:
            messages.error(request, "Tu cuenta de empresa no tiene perfil configurado.")
            return redirect("hola_mundo")

        ofert = OfertaLaboral.objects.filter(empresa=empresa).order_by('-fecha_publicacion')

    # ---------------------------------------------
    # SI ES CANDIDATO
    # ---------------------------------------------
    elif usuario.rol == "candidato":
        ofert = OfertaLaboral.objects.all().order_by('-fecha_publicacion')

    else:
        messages.error(request, "Tipo de usuario desconocido.")
        return redirect("hola_mundo")

    # Filtro de ubicación
    ubicacion = request.GET.get('ubicacion')
    if ubicacion:
        ofert = ofert.filter(ubicacion__icontains=ubicacion)

    paginator = Paginator(ofert, 10)
    page_number = request.GET.get('page')
    ofertas = paginator.get_page(page_number)

    ubicaciones = ofert.values_list('ubicacion', flat=True).distinct()

    return render(request, 'ofertas/index.html', {
    'ofertas': ofertas,
    'ubicaciones': ubicaciones,
    'es_empresa': es_empresa(request.user)
})
   



# =====================================================
# FORMULARIO PARA CREAR OFERTA (MODAL)
# =====================================================
@login_required(login_url='login')
def obtener_formulario_creacion(request):

    if not es_empresa(request.user):
        return JsonResponse({'success': False, 'error': 'No autorizado'}, status=403)

    formulario = Ofertasform()

    form_html = render(request, 'ofertas/form.html', {
        'formulario': formulario,
        'es_modal': True,
        'es_creacion': True
    }).content.decode('utf-8')

    return JsonResponse({'success': True, 'form_html': form_html})



# =====================================================
# FORMULARIO PARA EDITAR (MODAL)
# =====================================================
@login_required(login_url='login')
def obtener_formulario_edicion(request, id):

    if not es_empresa(request.user):
        return JsonResponse({'success': False, 'error': 'No autorizado'}, status=403)

    empresa = request.user.perfilempresa
    oferta = get_object_or_404(OfertaLaboral, id=id, empresa=empresa)

    formulario = Ofertasform(instance=oferta)

    form_html = render(request, 'ofertas/form.html', {
        'formulario': formulario,
        'oferta': oferta,
        'es_modal': True,
        'es_creacion': False
    }).content.decode('utf-8')

    return JsonResponse({'success': True, 'form_html': form_html, 'titulo': oferta.titulo})



# =====================================================
# GUARDAR NUEVA OFERTA (MODAL)
# =====================================================
@login_required(login_url='login')
def guardar_creacion_modal(request):

    if not es_empresa(request.user):
        return JsonResponse({'success': False, 'error': 'No autorizado'}, status=403)

    if request.method == 'POST':
        empresa = request.user.perfilempresa

        formulario = Ofertasform(request.POST, request.FILES)

        if formulario.is_valid():
            nueva_oferta = formulario.save(commit=False)
            nueva_oferta.empresa = empresa
            nueva_oferta.save()

            return JsonResponse({
                'success': True,
                'message': f'Oferta "{nueva_oferta.titulo}" creada correctamente'
            })

        form_html = render(request, 'ofertas/form.html', {
            'formulario': formulario,
            'es_modal': True,
            'es_creacion': True
        }).content.decode('utf-8')

        return JsonResponse({
            'success': False,
            'error': 'Por favor corrige los errores del formulario',
            'form_html': form_html
        })


# =====================================================
# GUARDAR EDICIÓN (MODAL)
# =====================================================
@login_required(login_url='login')
def guardar_edicion_modal(request, id):

    if not es_empresa(request.user):
        return JsonResponse({'success': False, 'error': 'No autorizado'}, status=403)

    if request.method == 'POST':

        empresa = request.user.perfilempresa
        oferta = get_object_or_404(OfertaLaboral, id=id, empresa=empresa)

        formulario = Ofertasform(request.POST, request.FILES, instance=oferta)

        if formulario.is_valid():
            oferta_guardada = formulario.save()

            return JsonResponse({
                'success': True,
                'message': f'Oferta "{oferta_guardada.titulo}" actualizada correctamente'
            })

        form_html = render(request, 'ofertas/form.html', {
            'formulario': formulario,
            'oferta': oferta,
            'es_modal': True,
            'es_creacion': False
        }).content.decode('utf-8')

        return JsonResponse({
            'success': False,
            'error': 'Por favor corrige los errores del formulario',
            'form_html': form_html
        })

    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)



# =====================================================
# ELIMINAR UNA OFERTA
# =====================================================
@login_required(login_url='login')
def eliminar(request, id):

    if not es_empresa(request.user):
        messages.error(request, "No autorizado.")
        return redirect('ofertas:ofertas')

    empresa = request.user.perfilempresa
    oferta = get_object_or_404(OfertaLaboral, id=id, empresa=empresa)

    oferta.delete()

    messages.success(request, "Oferta eliminada correctamente")
    return redirect('ofertas:ofertas')




#VISTAS PARA AGREGAR NUEVO DATO - Funcionalidad simple

#@login_required(login_url='login')
#def crear_oferta(request):
 #   if request.method == 'POST':
  #      formulario = Ofertasform(request.POST, request.FILES)
   #     if formulario.is_valid():
    #        formulario.save()
     #       messages.success(request, 'Oferta creada correctamente')
      #      return redirect('ofertas')
   # else:
    #    formulario = Ofertasform()
    
   # return render(request, 'ofertas/create.html', {'formulario': formulario})