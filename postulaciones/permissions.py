from ofertas.models import OfertaLaboral
from perfiles.models import PerfilCandidato, PerfilEmpresa
from postulaciones.models import Postulacion


def puede_postular_con_id(user, id):
    try:
        id = int(id)
    except ValueError:
        return False

    oferta = None
    try:
        oferta = OfertaLaboral.objects.get(id=id)
    except:
        return False

    if oferta is None:
        return False

    if not user.is_authenticated or user.rol != "candidato":
        return False

    perfil = PerfilCandidato.objects.filter(usuario_id=user.id).first()

    if perfil is None:
        return False

    postulacion_existente = None
    try:
        postulacion_existente = Postulacion.objects.filter(oferta=oferta, candidato=perfil).first()
    except:
        return False

    return postulacion_existente is None


def puede_cancelar_postulacion(user, id):
    try:
        id = int(id)
    except ValueError:
        return False

    oferta = None
    try:
        oferta = OfertaLaboral.objects.get(id=id)
    except OfertaLaboral.DoesNotExist:
        return False

    if oferta is None:
        return False

    if not user.is_authenticated:
        return False

    if user.rol != "candidato":
        return False

    perfil = PerfilCandidato.objects.filter(usuario_id=user.id).first()

    if perfil is None:
        return False

    postulacion = None
    try:
        postulacion = Postulacion.objects.get(oferta=oferta, candidato=perfil)
    except:
        return False

    if postulacion is None:
        return False

    return True


def puede_actualizar_postulacion(user, oferta_id, nuevo_estado, candidato_id):
    try:
        oferta_id = int(oferta_id)
    except ValueError:
        return False

    if nuevo_estado not in dict(Postulacion.ESTADOS).keys() or nuevo_estado == "pendiente":
        return False

    oferta = None
    try:
        oferta = OfertaLaboral.objects.get(id=oferta_id)
    except OfertaLaboral.DoesNotExist:
        return False

    if oferta is None:
        return False

    if not user.is_authenticated:
        return False

    if user.rol != "empresa":
        return False

    perfil = PerfilEmpresa.objects.filter(usuario_id=user.id).first()
    if perfil is None:
        return False

    if oferta.empresa != perfil:
        return False

    postulacion = None
    try:
        postulacion = Postulacion.objects.get(oferta=oferta, candidato_id=candidato_id)
    except:
        return False

    if postulacion is None:
        return False

    if postulacion.estado != "pendiente":
        return False

    return True
