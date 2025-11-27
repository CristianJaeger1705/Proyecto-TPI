from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import OfertaLaboral
from ofertas.forms import Ofertasform
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .decorators import empresa_o_admin_required
# Create your views here.
#Lista todos las vacantes disponibles
@empresa_o_admin_required
def ofertas_List(request):
    ofert = OfertaLaboral.objects.all().order_by('-fecha_publicacion')
           # Filtrar por ubicación
    ubicacion = request.GET.get('ubicacion')
    if ubicacion:
        ofert = ofert.filter(ubicacion__icontains=ubicacion)
    
    # Paginar - 10 registros por página
    paginator = Paginator(ofert, 10)
    # Obtener el número de página desde la URL
    page_number = request.GET.get('page')
    # Obtener la página actual
    ofertas = paginator.get_page(page_number)
    # Obtener ubicaciones únicas para el filtro
    ubicaciones = OfertaLaboral.objects.values_list('ubicacion', flat=True).distinct()

    return render(request, 'ofertas/index.html',{'ofertas': ofertas,'ubicaciones': ubicaciones })
#funcion para eliminar un campo o registro
@empresa_o_admin_required
def eliminar(request, id):
    ofert = OfertaLaboral.objects.get(id=id)
    nombre_oferta=ofert.titulo
    ofert.delete()
    return redirect('ofertas')


# =============================================================================
# VISTAS PARA UTILIZAR EL MODAL EDITAR Y AGREGAR NUEVO
# =============================================================================
@empresa_o_admin_required
def obtener_formulario_creacion(request):
    """Obtener formulario de creación para modal - NUEVA VISTA"""
    try:
        formulario = Ofertasform()
        
        form_html = render(request,'ofertas/form.html', {
            'formulario': formulario,
            'es_modal': True,
            'es_creacion': True  # Nueva variable para identificar creación
        }).content.decode('utf-8')
        
        return JsonResponse({
            'success': True,
            'form_html': form_html
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
    
@empresa_o_admin_required
def obtener_formulario_edicion(request, id):
    #Obtener formulario de edición para modal
    try:
        oferta = get_object_or_404(OfertaLaboral, id=id)
        formulario = Ofertasform(instance=oferta)
        
        form_html = render(request, 'ofertas/form.html', {
            'formulario': formulario,
            'oferta': oferta,
            'es_modal': True,
            'es_creacion': False  # No es creación, es edición
        }).content.decode('utf-8')
        
        return JsonResponse({
            'success': True,
            'form_html': form_html,
            'titulo': oferta.titulo
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@empresa_o_admin_required
def guardar_creacion_modal(request):
    #Guardar nueva oferta desde modal 
    if request.method == 'POST':
        try:
            formulario = Ofertasform(request.POST, request.FILES)
            
            if formulario.is_valid():
                nueva_oferta = formulario.save()
                return JsonResponse({
                    'success': True,
                    'message': f'Oferta "{nueva_oferta.titulo}" creada correctamente'
                })
            else:
                # Si hay errores, volver a renderizar el formulario
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
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    else:
        return JsonResponse({
            'success': False,
            'error': 'Método no permitido'
        }, status=405)

@empresa_o_admin_required
def guardar_edicion_modal(request, id):
    #Guardar cambios desde el modal
    if request.method == 'POST':
        try:
            oferta = get_object_or_404(OfertaLaboral, id=id)
            formulario = Ofertasform(request.POST, request.FILES, instance=oferta)
            
            if formulario.is_valid():
                oferta_guardada = formulario.save()
                return JsonResponse({
                    'success': True,
                    'message': f'Oferta "{oferta_guardada.titulo}" actualizada correctamente'
                })
            else:
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
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    else:
        return JsonResponse({
            'success': False,
            'error': 'Método no permitido'
        }, status=405)
    
#VISTAS PARA AGREGAR NUEVO DATO - Funcionalidad simple
@empresa_o_admin_required
def obtener_datos_visualizacion(request, id):
    """Obtener datos de oferta para modal de visualización"""
    try:
        oferta = get_object_or_404(OfertaLaboral, id=id)
        
        # Renderizar un template específico para visualización
        form_html = render(request, 'ofertas/ofertview.html', {
            'oferta': oferta,
            'es_modal': True
        }).content.decode('utf-8')
        
        return JsonResponse({
            'success': True,
            'form_html': form_html,
            'titulo': f"Visualizando: {oferta.titulo}"
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
    

    ####################################################################################
    # VISTA DE OFERTAS ABIERTAS AL PUBLICO 
    #####################################################################################

def lista_ofertas_publicas(request):
    ofertas = OfertaLaboral.objects.filter(estado='activa').order_by('-fecha_publicacion')

    contexto = {
        'ofertas': ofertas,
        'total_ofertas': ofertas.count()
    }
    return render(request, 'ofertas/ofertas_publicadas.html', contexto)