from itertools import count
import json
from urllib import request

from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from perfiles.models import RUBROS_EMPRESA, PerfilEmpresa
from postulaciones.permissions import puede_cancelar_postulacion, puede_postular_con_id
from postulaciones.views import obtener_postulantes_de_oferta

from .models import Favorito, OfertaLaboral
from .decorators import candidato_required, empresa_o_admin_required
from ofertas.forms import Ofertasform


# ============================================================
# LISTA OFERTAS DE LA EMPRESA
# ============================================================
@empresa_o_admin_required
def ofertas_List(request):

    empresa = get_object_or_404(PerfilEmpresa, usuario=request.user)

    ofert = OfertaLaboral.objects.filter(
        empresa=empresa
    ).order_by('-fecha_publicacion')

    # Filtrar por ubicación
    ubicacion = request.GET.get('ubicacion')
    if ubicacion:
        ofert = ofert.filter(ubicacion__icontains=ubicacion)

    # Paginar
    paginator = Paginator(ofert, 10)
    page_number = request.GET.get('page')
    ofertas = paginator.get_page(page_number)

    # Ubicaciones únicas
    ubicaciones = OfertaLaboral.objects.filter(
        empresa=empresa
    ).values_list('ubicacion', flat=True).distinct()

    return render(request, 'ofertas/index.html', {
        'ofertas': ofertas,
        'ubicaciones': ubicaciones
    })


# ============================================================
# ELIMINAR OFERTA
# ============================================================
@empresa_o_admin_required
def eliminar(request, id):
    empresa = get_object_or_404(PerfilEmpresa, usuario=request.user)
    ofert = get_object_or_404(OfertaLaboral, id=id, empresa=empresa)
    ofert.delete()
    return redirect('ofertas')


# ============================================================
# FORMULARIO CREACIÓN PARA MODAL
# ============================================================
@empresa_o_admin_required
def obtener_formulario_creacion(request):
    try:
        Ofertasform()
        formulario = Ofertasform()

        form_html = render(
            request,
            'ofertas/form.html',
            {
                'formulario': formulario,
                'es_modal': True,
                'es_creacion': True
            }
        ).content.decode('utf-8')

        return JsonResponse({
            'success': True,
            'form_html': form_html
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ============================================================
# FORMULARIO EDICIÓN PARA MODAL
# ============================================================
@empresa_o_admin_required
def obtener_formulario_edicion(request, id):
    try:
        empresa = get_object_or_404(PerfilEmpresa, usuario=request.user)
        oferta = get_object_or_404(OfertaLaboral, id=id, empresa=empresa)

        formulario = Ofertasform(instance=oferta)

        form_html = render(
            request,
            'ofertas/form.html',
            {
                'formulario': formulario,
                'oferta': oferta,
                'es_modal': True,
                'es_creacion': False
            }
        ).content.decode('utf-8')

        return JsonResponse({
            'success': True,
            'form_html': form_html,
            'titulo': oferta.titulo
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ============================================================
# GUARDAR NUEVA OFERTA (MODAL)
# ============================================================
@empresa_o_admin_required
def guardar_creacion_modal(request):

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    try:
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

        # Formulario inválido
        form_html = render(
            request,
            'ofertas/form.html',
            {
                'formulario': formulario,
                'es_modal': True,
                'es_creacion': True
            }
        ).content.decode('utf-8')

        return JsonResponse({
            'success': False,
            'error': 'Por favor corrige los errores del formulario',
            'form_html': form_html
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ============================================================
# GUARDAR EDICIÓN (MODAL)
# ============================================================
@empresa_o_admin_required
def guardar_edicion_modal(request, id):

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

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

        # Formulario inválido
        form_html = render(
            request,
            'ofertas/form.html',
            {
                'formulario': formulario,
                'oferta': oferta,
                'es_modal': True,
                'es_creacion': False
            }
        ).content.decode('utf-8')

        return JsonResponse({
            'success': False,
            'error': 'Por favor corrige los errores del formulario',
            'form_html': form_html
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ============================================================
# VISUALIZAR OFERTA (MODAL)
# ============================================================
@empresa_o_admin_required
def obtener_datos_visualizacion(request, id):

    try:
        empresa = get_object_or_404(PerfilEmpresa, usuario=request.user)
        oferta = get_object_or_404(OfertaLaboral, id=id, empresa=empresa)

        acciones = {
            'puedePostular': puede_postular_con_id(request.user, id),
            'puedeCancelarPostulacion': puede_cancelar_postulacion(request.user, id),
        }

        form_html = render(
            request,
            'ofertas/ofertview.html',
            {
                'oferta': oferta,
                'es_modal': True,
                'acciones': acciones
            }
        ).content.decode('utf-8')

        return JsonResponse({
            'success': True,
            'form_html': form_html,
            'titulo': f"Visualizando: {oferta.titulo}"
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ============================================================
# LISTA OFERTAS PÚBLICAS
# ============================================================
def lista_ofertas_publicas(request):

    rubro_seleccionado = request.GET.get('rubro', '')
    orden = request.GET.get('orden')

    base_queryset = OfertaLaboral.objects.select_related('empresa').filter(
        estado='activa'
    )

    # Filtro por rubro
    if rubro_seleccionado:
        base_queryset = base_queryset.filter(empresa__rubro=rubro_seleccionado)

    # Orden
    if orden == 'reciente':
        base_queryset = base_queryset.order_by('-fecha_publicacion')
    elif orden == 'vencimiento':
        base_queryset = base_queryset.order_by('fecha_expiracion')
    else:
        base_queryset = base_queryset.order_by('-fecha_publicacion')

    paginator = Paginator(base_queryset, 10)
    page_number = request.GET.get('page')
    ofertas = paginator.get_page(page_number)

    # Categorías
    categorias = []
    for rubro_id, rubro_nombre in RUBROS_EMPRESA:
        count_total = OfertaLaboral.objects.filter(
            estado='activa',
            empresa__rubro=rubro_id
        ).count()

        if count_total > 0:
            categorias.append({
                'id': rubro_id,
                'nombre': rubro_nombre,
                'total': count_total,
                'activo': rubro_id == rubro_seleccionado
            })

    todas_categorias = {
        'id': '',
        'nombre': 'Todas las categorías',
        'total': OfertaLaboral.objects.filter(estado='activa').count(),
        'activo': not rubro_seleccionado
    }

    # Favoritos
    favoritos_ids = []

    if request.user.is_authenticated:
        favoritos_ids = list(
            Favorito.objects.filter(usuario=request.user)
            .values_list('oferta_id', flat=True)
        )
    else:
        raw_cookie = request.COOKIES.get('favoritos_laburosv')
        if raw_cookie:
            try:
                data = json.loads(raw_cookie)
                favoritos_ids = [
                    int(x) for x in data
                    if str(x).isdigit()
                ]
            except:
                favoritos_ids = []

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

    response = render(request, 'ofertas/ofertas_publicadas.html', contexto)

    if not request.user.is_authenticated and favoritos_ids:
        response.set_cookie(
            'favoritos_laburosv',
            json.dumps(favoritos_ids),
            max_age=60 * 60 * 24 * 90,
            httponly=False,
            samesite='Lax'
        )

    return response


# ============================================================
# VER OFERTA PÚBLICA
# ============================================================
def ver_oferta_publica(request, oferta_id):

    acciones = {
        'puedePostular': puede_postular_con_id(request.user, oferta_id),
        'puedeCancelarPostulacion': puede_cancelar_postulacion(request.user, oferta_id),
    }

    postulantes = obtener_postulantes_de_oferta(request, oferta_id)
    oferta = get_object_or_404(OfertaLaboral, id=oferta_id)

    esta_en_favoritos = False

    if request.user.is_authenticated:
        esta_en_favoritos = Favorito.objects.filter(
            usuario=request.user,
            oferta=oferta
        ).exists()
    else:
        raw_cookie = request.COOKIES.get('favoritos_laburosv')
        if raw_cookie:
            try:
                data = json.loads(raw_cookie)
                esta_en_favoritos = oferta_id in [
                    int(x) for x in data if str(x).isdigit()
                ]
            except:
                esta_en_favoritos = False

    ofertas_similares = OfertaLaboral.objects.filter(
        empresa__rubro=oferta.empresa.rubro,
        estado='activa'
    ).exclude(id=oferta_id)[:3]
    return render(
        request,
        'ofertas/detalle_oferta_publica.html',
        {
            'oferta': oferta,
            'acciones': acciones,
            'postulantes': postulantes,
            'esta_en_favoritos': esta_en_favoritos,
            'ofertas_similares': ofertas_similares,
        }
    )


# ============================================================
# TOGGLE FAVORITOS
# ============================================================
def toggle_favorito(request, oferta_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

    try:
        oferta = get_object_or_404(OfertaLaboral, id=oferta_id)

        # --- Usuario autenticado ---
        if request.user.is_authenticated:
            # Solo candidatos pueden guardar favoritos
            if request.user.rol != 'candidato':
                return JsonResponse({
                    'success': False, 
                    'error': 'Solo los candidatos pueden guardar favoritos'
                }, status=403)
                
            fav, created = Favorito.objects.get_or_create(
                usuario=request.user,
                oferta=oferta
            )
            if not created:
                fav.delete()
                agregado = False
            else:
                agregado = True

            total = Favorito.objects.filter(usuario=request.user).count()

            return JsonResponse({
                'success': True,
                'agregado': agregado,
                'total': total
            })

        # --- Usuario anónimo ---
        cookie_name = 'favoritos_laburosv'
        cookie_raw = request.COOKIES.get(cookie_name, '[]')

        try:
            favoritos = json.loads(cookie_raw)
            favoritos = [int(x) for x in favoritos if str(x).isdigit()]
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
            'total': len(favoritos),
            'needs_login': True  # ← ESTE ES EL CAMPO IMPORTANTE
        })

        response.set_cookie(
            cookie_name,
            json.dumps(favoritos),
            max_age=60 * 60 * 24 * 90,
            httponly=False,
            samesite='Lax'
        )

        return response

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# ============================================================
# FAVORITOS DE CANDIDATO
# ============================================================
@candidato_required
def mis_favoritos(request):

    mis_favs = request.user.favoritos.select_related(
        'oferta',
        'oferta__empresa'
    ).order_by('-fecha')

    ofertas_favoritas = [f.oferta for f in mis_favs]

    return render(
        request,
        'ofertas/mis_favoritos.html',
        {
            'ofertas': ofertas_favoritas,
            'total_favoritos': len(ofertas_favoritas)
        }
    )


# ============================================================
# FUNCIÓN AUXILIAR
# ============================================================
def obtener_total_favoritos(request):

    if request.user.is_authenticated:
        return Favorito.objects.filter(usuario=request.user).count()

    try:
        favs = json.loads(request.COOKIES.get('favoritos_laburosv', '[]'))
        return len(favs)
    except:
        return 0


# ============================================================
# CHECK AUTH (JS)
# ============================================================
def check_auth(request):

    return JsonResponse({
        'is_authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else None
    })


# ============================================================
# INICIAR CHAT (PARTE DE MENSAJERÍA)
# ============================================================
@login_required
def iniciar_chat(request, oferta_id):

    from mensajeria.models import Chat  # evitar import circular

    oferta = get_object_or_404(OfertaLaboral, id=oferta_id)
    empresa = oferta.empresa.usuario

    chat, creado = Chat.objects.get_or_create(
        es_grupal=False,
        defaults={'nombre': f'Chat con {empresa.username}'}
    )
    chat.participantes.add(request.user, empresa)
    chat.save()

    return redirect('mensajeria:chat-detalle', chat.id)
