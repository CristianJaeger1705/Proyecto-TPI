from itertools import count
import json
from urllib import request
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from perfiles.models import RUBROS_EMPRESA
from postulaciones.permissions import puede_cancelar_postulacion, puede_postular_con_id
from postulaciones.views import obtener_postulantes_de_oferta
from .models import Favorito, OfertaLaboral
from ofertas.forms import Ofertasform
from django.core.paginator import Paginator

from .decorators import candidato_required, empresa_o_admin_required
from perfiles.models import PerfilEmpresa
from postulaciones.permissions import puede_postular_con_id, puede_cancelar_postulacion

# Create your views here.
#Lista todos las vacantes disponibles
@empresa_o_admin_required
def ofertas_List(request):

    # Filtrar solo las ofertas de la empresa logueada
    ofert = OfertaLaboral.objects.filter(empresa=request.user.perfil_empresa).order_by('-fecha_publicacion')
    
    # Filtrar por ubicación (solo dentro de las ofertas de la empresa)
    empresa = get_object_or_404(PerfilEmpresa, usuario=request.user)
    ofert = OfertaLaboral.objects.filter(empresa=empresa).order_by('-fecha_publicacion')
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
    
    # Obtener ubicaciones únicas SOLO de las ofertas de esta empresa
    ubicaciones = OfertaLaboral.objects.filter(empresa=request.user.perfil_empresa).values_list('ubicacion', flat=True).distinct()

    return render(request, 'ofertas/index.html', {'ofertas': ofertas, 'ubicaciones': ubicaciones})
#funcion para eliminar un campo o registro
@empresa_o_admin_required
def eliminar(request, id):
    empresa = get_object_or_404(PerfilEmpresa, usuario=request.user)
    ofert = get_object_or_404(OfertaLaboral, id=id, empresa=empresa)
    ofert.delete()
    return redirect('ofertas')


# =============================================================================
# VISTAS PARA UTILIZAR EL MODAL EDITAR Y AGREGAR NUEVO
# =============================================================================
@empresa_o_admin_required
def obtener_formulario_creacion(request):
    """Obtener formulario de creación para modal - NUEVA VISTA"""
    try:
        get_object_or_404(PerfilEmpresa, usuario=request.user)
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
        empresa = get_object_or_404(PerfilEmpresa, usuario=request.user)
        oferta = get_object_or_404(OfertaLaboral, id=id, empresa=empresa)
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
    # Guardar nueva oferta desde modal 
    if request.method == 'POST':
        try:
            # PASAR EL REQUEST al formulario para que asigne automáticamente la empresa
            formulario = Ofertasform(request.POST, request.FILES, request=request)
            
            if formulario.is_valid():
                nueva_oferta = formulario.save(commit=False)
                perfil_empresa = get_object_or_404(PerfilEmpresa, usuario=request.user)
                nueva_oferta.empresa = perfil_empresa
                nueva_oferta.save()
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
            empresa = get_object_or_404(PerfilEmpresa, usuario=request.user)
            oferta = get_object_or_404(OfertaLaboral, id=id, empresa=empresa)
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
        empresa = get_object_or_404(PerfilEmpresa, usuario=request.user)
        oferta = get_object_or_404(OfertaLaboral, id=id, empresa=empresa)

        acciones = {
            'puedePostular': puede_postular_con_id(request.user, id),
            'puedeCancelarPostulacion': puede_cancelar_postulacion(request.user, id),
        }

        form_html = render(request, 'ofertas/ofertview.html', {
            'oferta': oferta,
            'es_modal': True,
            'acciones': acciones
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
    # VISTA DE OFERTAS ABIERTAS AL PUBLICO NO REQUIERE INICIAR SESION
    # CUALQUIER PERSONA PUEDE VERLO
    #####################################################################################
def lista_ofertas_publicas(request):
    rubro_seleccionado = request.GET.get('rubro', '')
    orden = request.GET.get('orden')
    
    # Consulta base
    base_queryset = OfertaLaboral.objects.select_related('empresa').filter(
        estado='activa'
    )

    # Filtro por rubro
    if rubro_seleccionado:
        base_queryset = base_queryset.filter(empresa__rubro=rubro_seleccionado)
    
    # ORDENAMIENTO
    if orden == 'reciente':
        base_queryset = base_queryset.order_by('-fecha_publicacion')
    elif orden == 'vencimiento':
        base_queryset = base_queryset.order_by('fecha_expiracion')
    else:
        base_queryset = base_queryset.order_by('-fecha_publicacion')
    
    # PAGINACIÓN
    paginator = Paginator(base_queryset, 10)
    page_number = request.GET.get('page')
    ofertas = paginator.get_page(page_number)
    
    # CATEGORÍAS
    categorias = []
    for rubro_id, rubro_nombre in RUBROS_EMPRESA:
        count = OfertaLaboral.objects.filter(estado='activa', empresa__rubro=rubro_id).count()
        if count > 0:
            categorias.append({
                'id': rubro_id,
                'nombre': rubro_nombre,
                'total': count,
                'activo': rubro_id == rubro_seleccionado
            })

    todas_categorias = {
        'id': '',
        'nombre': 'Todas las categorías',
        'total': OfertaLaboral.objects.filter(estado='activa').count(),
        'activo': not rubro_seleccionado
    }

    # FAVORITOS: versión 100% segura y sin errores
    favoritos_ids = []

    if request.user.is_authenticated:
        favoritos_ids = list(
            Favorito.objects.filter(usuario=request.user)
            .values_list('oferta_id', flat=True)
        )
    else:
        raw_cookie = request.COOKIES.get('favoritos_laburosv')
        if raw_cookie and raw_cookie.strip():
            try:
                data = json.loads(raw_cookie)
                if isinstance(data, list):
                    favoritos_ids = [int(x) for x in data if isinstance(x, (int, str)) and str(x).isdigit()]
            except (json.JSONDecodeError, ValueError, TypeError):
                favoritos_ids = []  # Cookie corrupta → ignorar
        # Si no hay cookie o está vacía → favoritos_ids queda como lista vacía

    # CONTEXTO
    contexto = {
        'ofertas': ofertas,
        'categorias': categorias,
        'todas_categorias': todas_categorias,
        'rubro_seleccionado': rubro_seleccionado,
        'total_ofertas': base_queryset.count(),
        'orden_actual': orden,
        'favoritos_ids': favoritos_ids,
        'total_favoritos': len(favoritos_ids),
        'es_autenticado': request.user.is_authenticated,
    }

    # RESPUESTA + cookie para anónimos
    response = render(request, 'ofertas/ofertas_publicadas.html', contexto)

    if not request.user.is_authenticated and favoritos_ids:
        response.set_cookie(
            'favoritos_laburosv',
            json.dumps(favoritos_ids),
            max_age=60*60*24*90,  # 90 días
            httponly=False,
            samesite='Lax'
        )

    return response

def ver_oferta_publica(request, oferta_id):
    acciones = {
        'puedePostular': puede_postular_con_id(request.user, oferta_id),
        'puedeCancelarPostulacion': puede_cancelar_postulacion(request.user, oferta_id),
    }

    postulantes = obtener_postulantes_de_oferta(request, oferta_id)
    oferta = get_object_or_404(OfertaLaboral, id=oferta_id)
    
    # SOLO VERIFICAR SI ESTÁ EN FAVORITOS (sin toda la lógica de cookies)
    esta_en_favoritos = False
    
    if request.user.is_authenticated:
        # Usuario autenticado: verificar en BD
        esta_en_favoritos = Favorito.objects.filter(
            usuario=request.user, 
            oferta=oferta
        ).exists()
    else:
        # Usuario anónimo: verificar en cookie
        raw_cookie = request.COOKIES.get('favoritos_laburosv')
        if raw_cookie:
            try:
                favoritos = json.loads(raw_cookie)
                esta_en_favoritos = oferta_id in [int(f) for f in favoritos if str(f).isdigit()]
            except:
                esta_en_favoritos = False
    
    # Obtener ofertas similares (opcional)
    ofertas_similares = OfertaLaboral.objects.filter(
        empresa__rubro=oferta.empresa.rubro,
        estado='activa'
    ).exclude(id=oferta_id)[:3]
    
    return render(request, 'ofertas/detalle_oferta_publica.html', {
        'oferta': oferta, 
        'acciones': acciones, 
        'postulantes': postulantes,
        'esta_en_favoritos': esta_en_favoritos,  # ← NUEVO: solo booleano
        'ofertas_similares': ofertas_similares,
    })


@csrf_exempt
def toggle_favorito(request, oferta_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    try:
        oferta = get_object_or_404(OfertaLaboral, id=oferta_id)
        
        if request.user.is_authenticated:
            fav, created = Favorito.objects.get_or_create(
                usuario=request.user,
                oferta=oferta
            )
            if not created:
                fav.delete()
                agregado = False
            else:
                agregado = True
        else:
            # Manejo para usuarios anónimos
            cookie_name = 'favoritos_laburosv'
            cookie_data = request.COOKIES.get(cookie_name, '[]')
            
            try:
                favoritos = json.loads(cookie_data)
                favoritos = [int(f) for f in favoritos if str(f).isdigit()]
            except:
                favoritos = []
            
            if oferta_id in favoritos:
                favoritos.remove(oferta_id)
                agregado = False
            else:
                favoritos.append(oferta_id)
                agregado = True
            
            response = JsonResponse({
                'success': True,
                'agregado': agregado,
                'total': len(favoritos)
            })
            
            response.set_cookie(
                cookie_name,
                json.dumps(favoritos),
                max_age=60*60*24*90,
                httponly=False,
                samesite='Lax'
            )
            
            return response
        
        total = obtener_total_favoritos(request)
        return JsonResponse({
            'success': True,
            'agregado': agregado,
            'total': total
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@candidato_required
def mis_favoritos(request):
    mis_favs = request.user.favoritos.select_related('oferta', 'oferta__empresa').order_by('-fecha')
    ofertas_favoritas = [f.oferta for f in mis_favs]
    return render(request, 'ofertas/mis_favoritos.html', {
        'ofertas': ofertas_favoritas,
        'total_favoritos': len(ofertas_favoritas)
    })



# ← FUNCIÓN AUXILIAR (pégala también)
def obtener_total_favoritos(request):
    if request.user.is_authenticated:
        return Favorito.objects.filter(usuario=request.user).count()
    else:
        try:
            favs = json.loads(request.COOKIES.get('favoritos_laburosv', '[]'))
            return len(favs)
        except:
            return 0
def check_auth(request):
    """Verificar si el usuario está autenticado (para JS)"""
    return JsonResponse({
        'is_authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else None
    })