from django.db.models.signals import post_save
from django.dispatch import receiver
from perfiles.models import PerfilEmpresa
from usuarios.models import Usuario
from mensajeria.models import Chat, Notificacion
from django.utils import timezone

GRUPO_GENERAL_NOMBRE = "Grupo General: Empresas y Admins"

def crear_o_actualizar_grupo_general():
    """
    Crea o actualiza un grupo general con todas las empresas y todos los admins.
    Cada empresa nueva genera una notificación para los admins.
    """
    # Obtener o crear grupo
    grupo, created = Chat.objects.get_or_create(
        nombre=GRUPO_GENERAL_NOMBRE,
        es_grupal=True
    )

    # Obtener participantes actuales
    participantes_actuales = set(grupo.participantes.all())

    # Todos los admins y todas las empresas
    admins = set(Usuario.objects.filter(rol='admin'))
    empresas = set(Usuario.objects.filter(perfil_empresa__isnull=False))

    # Empresas nuevas que no están en el grupo
    nuevas_empresas = empresas - participantes_actuales

    # Agregar nuevas empresas y todos los admins
    grupo.participantes.add(*list(nuevas_empresas | admins))
    grupo.save()

    # Crear notificaciones solo para nuevas empresas agregadas
    for empresa in nuevas_empresas:
        for admin in admins:
            Notificacion.objects.create(
                usuario=admin,
                tipo="Empresa agregada al grupo",
                mensaje=f"Se agregó la empresa '{empresa.perfil_empresa.nombre_empresa}' al grupo general a las {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}"
            )

    # Crear notificación de creación del grupo solo si se creó ahora
    if created:
        for admin in admins:
            Notificacion.objects.create(
                usuario=admin,
                tipo="Grupo general creado",
                mensaje=f"Se creó el grupo general con todos los admins y empresas a las {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}"
            )

# SIGNAL: cada vez que se crea un PerfilEmpresa, actualizar el grupo general
@receiver(post_save, sender=PerfilEmpresa)
def actualizar_grupo_general_al_crear_empresa(sender, instance, created, **kwargs):
    crear_o_actualizar_grupo_general()


# ==========================================
# SCRIPT PARA NOTIFICACIONES HISTÓRICAS
# ==========================================
def generar_notificaciones_historicas():
    """
    Crea notificaciones para todas las empresas que ya estaban en el grupo general,
    de manera que el admin vea todas las empresas aunque sean antiguas.
    """
    try:
        grupo = Chat.objects.get(nombre=GRUPO_GENERAL_NOMBRE, es_grupal=True)
    except Chat.DoesNotExist:
        print("No existe el grupo general. Se debe crear primero.")
        return

    admins = Usuario.objects.filter(rol='admin')
    empresas_en_grupo = grupo.participantes.filter(perfil_empresa__isnull=False)

    for empresa in empresas_en_grupo:
        for admin in admins:
            # Evitar duplicados: solo crear si no existe ya
            if not Notificacion.objects.filter(
                usuario=admin,
                tipo="Empresa agregada al grupo",
                mensaje__icontains=empresa.perfil_empresa.nombre_empresa
            ).exists():
                Notificacion.objects.create(
                    usuario=admin,
                    tipo="Empresa agregada al grupo",
                    mensaje=f"Empresa '{empresa.perfil_empresa.nombre_empresa}' se agregó al grupo general (registro histórico)"
                )

# Para ejecutar este script: abrir Django shell y llamar
# >>> from mensajeria.signals import generar_notificaciones_historicas
# >>> generar_notificaciones_historicas()
