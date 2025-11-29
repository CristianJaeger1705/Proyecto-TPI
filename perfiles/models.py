# perfiles/models.py
from django.db import models
from usuarios.models import Usuario
from django.db.models.signals import post_save
from django.dispatch import receiver

DEPARTAMENTOS_EL_SALVADOR = [
    ('ahuachapan', 'Ahuachapán'),
    ('cabanas', 'Cabañas'),
    # ... resto de departamentos ...
]

RUBROS_EMPRESA = [
    ('tecnologia', 'Tecnología e Informática'),
    ('construccion', 'Construcción'),
    # ... resto de rubros ...
]

TIPOS_EMPLEO = [
    ('tiempo_completo', 'Tiempo Completo'),
    ('medio_tiempo', 'Medio Tiempo'),
    # ... resto de tipos ...
]

SECTORES_INDUSTRIA = [
    ('tecnologia', 'Tecnología e Informática'),
    ('construccion', 'Construcción e Ingeniería'),
    # ... resto de sectores ...
]

# ============================================
# MODELO: PERFIL CANDIDATO
# ============================================

class PerfilCandidato(models.Model):
    """
    Perfil extendido para candidatos. Se crea automáticamente al registrarse.
    """
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='perfil_candidato',
        verbose_name='Usuario'
    )
    
    # Información personal
    telefono = models.CharField(max_length=15, blank=True, verbose_name='Teléfono')
    fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name='Fecha de Nacimiento')
    departamento = models.CharField(max_length=50, choices=DEPARTAMENTOS_EL_SALVADOR, blank=True, verbose_name='Departamento')
    municipio = models.CharField(max_length=100, blank=True, verbose_name='Municipio')
    direccion = models.TextField(blank=True, verbose_name='Dirección')
    
    # Información profesional
    profesion = models.CharField(max_length=200, blank=True, verbose_name='Profesión u Oficio')
    biografia = models.TextField(blank=True, verbose_name='Sobre mí')
    habilidades = models.TextField(blank=True, verbose_name='Habilidades', help_text='Separa tus habilidades con comas. Ej: Python, Django, SQL')
    experiencia = models.TextField(blank=True, verbose_name='Experiencia resumida')  # de la rama frank2
    cv_url = models.TextField(blank=True, null=True, verbose_name='CV URL')  # de la rama frank2

    # Educación
    nivel_educacion = models.CharField(
        max_length=50,
        choices=[
            ('primaria', 'Primaria'),
            ('secundaria', 'Secundaria/Bachillerato'),
            ('tecnico', 'Técnico'),
            ('universitario', 'Universitario'),
            ('postgrado', 'Postgrado'),
        ],
        blank=True,
        verbose_name='Nivel de Educación'
    )
    institucion_educativa = models.CharField(max_length=200, blank=True, verbose_name='Institución Educativa')

    # Archivos
    cv = models.FileField(upload_to='cvs/', blank=True, null=True, verbose_name='CV (PDF)')
    foto_perfil = models.ImageField(upload_to='fotos_perfil/candidatos/', blank=True, null=True, verbose_name='Foto de Perfil')

    # Disponibilidad
    disponibilidad = models.CharField(
        max_length=50,
        choices=[
            ('inmediata', 'Disponibilidad Inmediata'),
            ('dos_semanas', 'En 2 semanas'),
            ('un_mes', 'En 1 mes'),
            ('buscando', 'Solo explorando opciones'),
        ],
        default='inmediata',
        verbose_name='Disponibilidad'
    )
    
    salario_esperado = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Salario Esperado (USD)')
    
    # Metadata
    perfil_completo = models.BooleanField(default=False, verbose_name='Perfil Completo')
    completado = models.BooleanField(default=False)  # de la rama frank2
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Perfil de Candidato'
        verbose_name_plural = 'Perfiles de Candidatos'
        ordering = ['-fecha_actualizacion']
    
    def __str__(self):
        return f"Perfil de {self.usuario.get_full_name() or self.usuario.username}"
    
    def get_habilidades_lista(self):
        if self.habilidades:
            return [h.strip() for h in self.habilidades.split(',')]
        return []

    def verificar_completitud(self):
        campos_requeridos = [
            self.telefono,
            self.departamento,
            self.profesion,
            self.biografia,
            self.habilidades,
        ]
        self.perfil_completo = all(campos_requeridos)
        self.completado = self.perfil_completo
        self.save()
        return self.perfil_completo

# ============================================
# MODELO: PERFIL EMPRESA
# ============================================

class PerfilEmpresa(models.Model):
    """
    Perfil extendido para empresas y MYPEs. Se crea automáticamente al registrarse.
    """
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_empresa', verbose_name='Usuario')
    
    nombre_empresa = models.CharField(max_length=200, verbose_name='Nombre de la Empresa')
    rubro = models.CharField(max_length=50, choices=RUBROS_EMPRESA, blank=True, verbose_name='Rubro')
    descripcion = models.TextField(blank=True, verbose_name='Descripción de la Empresa')
    sitio_web = models.CharField(max_length=200, blank=True, verbose_name='Sitio Web')
    contacto = models.CharField(max_length=100, blank=True, verbose_name='Teléfono/Correo')
    verificada = models.BooleanField(default=False, verbose_name='Empresa Verificada')
    logo = models.ImageField(upload_to='logos_empresas/', blank=True, null=True, verbose_name='Logo')
    completado = models.BooleanField(default=False)

    # Metadata
    perfil_completo = models.BooleanField(default=False)
    activa = models.BooleanField(default=True, verbose_name='Empresa Activa')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Perfil de Empresa'
        verbose_name_plural = 'Perfiles de Empresas'
        ordering = ['-fecha_actualizacion']

    def __str__(self):
        return self.nombre_empresa or f"Empresa de {self.usuario.username}"

    def verificar_completitud(self):
        campos_requeridos = [
            self.nombre_empresa,
            self.rubro,
            self.descripcion,
            self.contacto,
        ]
        self.perfil_completo = all(campos_requeridos)
        self.completado = self.perfil_completo
        self.save()
        return self.perfil_completo

# ============================================
# SEÑALES: Auto-crear perfiles al registrarse
# ============================================

@receiver(post_save, sender=Usuario)
def crear_perfil_automatico(sender, instance, created, **kwargs):
    if created:
        if instance.rol == 'candidato':
            PerfilCandidato.objects.create(usuario=instance)
        elif instance.rol == 'empresa':
            PerfilEmpresa.objects.create(
                usuario=instance,
                nombre_empresa=instance.first_name or 'Mi Empresa'
            )
