# Create your models here.
from django.db import models
from usuarios.models import Usuario
from django.db.models.signals import post_save
from django.dispatch import receiver

DEPARTAMENTOS_EL_SALVADOR = [
    ('ahuachapan', 'Ahuachapán'),
    ('cabanas', 'Cabañas'),
    ('chalatenango', 'Chalatenango'),
    ('cuscatlan', 'Cuscatlán'),
    ('la_libertad', 'La Libertad'),
    ('la_paz', 'La Paz'),
    ('la_union', 'La Unión'),
    ('morazan', 'Morazán'),
    ('san_miguel', 'San Miguel'),
    ('san_salvador', 'San Salvador'),
    ('san_vicente', 'San Vicente'),
    ('santa_ana', 'Santa Ana'),
    ('sonsonate', 'Sonsonate'),
    ('usulutan', 'Usulután'),
]

RUBROS_EMPRESA = [
    ('tecnologia', 'Tecnología e Informática'),
    ('construccion', 'Construcción'),
    ('comercio', 'Comercio y Ventas'),
    ('restaurante', 'Restaurantes y Alimentos'),
    ('servicios', 'Servicios Profesionales'),
    ('manufactura', 'Manufactura'),
    ('agricultura', 'Agricultura'),
    ('educacion', 'Educación'),
    ('salud', 'Salud'),
    ('transporte', 'Transporte y Logística'),
    ('turismo', 'Turismo y Hotelería'),
    ('otro', 'Otro'),
]

# Municipios por departamento en El Salvador
MUNICIPIOS_POR_DEPARTAMENTO = {
    'ahuachapan': ['Ahuachapán', 'Apaneca', 'Atiquizaya', 'Concepción de Ataco', 'El Refugio', 'Guaymango', 'Jujutla', 'San Francisco Menéndez', 'San Lorenzo', 'San Pedro Puxtla', 'Tacuba', 'Turín'],
    'cabanas': ['Sensuntepeque', 'Cinquera', 'Dolores', 'Guacotecti', 'Ilobasco', 'Jutiapa', 'San Isidro', 'Tejutepeque', 'Victoria'],
    'chalatenango': ['Chalatenango', 'Agua Caliente', 'Arcatao', 'Azacualpa', 'Cancasque', 'Citalá', 'Comalapa', 'Concepción Quezaltepeque', 'Dulce Nombre de María', 'El Carrizal', 'El Paraíso', 'La Laguna', 'La Palma', 'La Reina', 'Las Vueltas', 'Nombre de Jesús', 'Nueva Concepción', 'Nueva Trinidad', 'Ojos de Agua', 'Potonico', 'San Antonio de la Cruz', 'San Antonio Los Ranchos', 'San Fernando', 'San Francisco Lempa', 'San Francisco Morazán', 'San Ignacio', 'San Isidro Labrador', 'San Luis del Carmen', 'San Miguel de Mercedes', 'San Rafael', 'Santa Rita', 'Tejutla'],
    'cuscatlan': ['Cojutepeque', 'Candelaria', 'El Carmen', 'El Rosario', 'Monte San Juan', 'Oratorio de Concepción', 'San Bartolomé Perulapía', 'San Cristóbal', 'San José Guayabal', 'San Pedro Perulapán', 'San Rafael Cedros', 'San Ramón', 'Santa Cruz Analquito', 'Santa Cruz Michapa', 'Suchitoto', 'Tenancingo'],
    'la_libertad': ['Santa Tecla', 'Antiguo Cuscatlán', 'Chiltiupán', 'Ciudad Arce', 'Colón', 'Comasagua', 'Huizúcar', 'Jayaque', 'Jicalapa', 'La Libertad', 'Nuevo Cuscatlán', 'Quezaltepeque', 'Sacacoyo', 'San José Villanueva', 'San Juan Opico', 'San Matías', 'San Pablo Tacachico', 'Talnique', 'Tamanique', 'Teotepeque', 'Tepecoyo', 'Zaragoza'],
    'la_paz': ['Zacatecoluca', 'Cuyultitán', 'El Rosario', 'Jerusalén', 'Mercedes La Ceiba', 'Olocuilta', 'Paraíso de Osorio', 'San Antonio Masahuat', 'San Emigdio', 'San Francisco Chinameca', 'San Juan Nonualco', 'San Juan Talpa', 'San Juan Tepezontes', 'San Luis La Herradura', 'San Luis Talpa', 'San Miguel Tepezontes', 'San Pedro Masahuat', 'San Pedro Nonualco', 'San Rafael Obrajuelo', 'Santa María Ostuma', 'Santiago Nonualco', 'Tapalhuaca'],
    'la_union': ['La Unión', 'Anamorós', 'Bolívar', 'Concepción de Oriente', 'Conchagua', 'El Carmen', 'El Sauce', 'Intipucá', 'Lislique', 'Meanguera del Golfo', 'Nueva Esparta', 'Pasaquina', 'Polorós', 'San Alejo', 'San José', 'Santa Rosa de Lima', 'Yayantique', 'Yucuaiquín'],
    'morazan': ['San Francisco Gotera', 'Arambala', 'Cacaopera', 'Chilanga', 'Corinto', 'Delicias de Concepción', 'El Divisadero', 'El Rosario', 'Gualococti', 'Guatajiagua', 'Joateca', 'Jocoaitique', 'Jocoro', 'Lolotiquillo', 'Meanguera', 'Osicala', 'Perquín', 'San Carlos', 'San Fernando', 'San Isidro', 'San Simón', 'Sensembra', 'Sociedad', 'Torola', 'Yamabal', 'Yoloaiquín'],
    'san_miguel': ['San Miguel', 'Carolina', 'Chapeltique', 'Chinameca', 'Chirilagua', 'Ciudad Barrios', 'Comacarán', 'El Tránsito', 'Lolotique', 'Moncagua', 'Nueva Guadalupe', 'Nuevo Edén de San Juan', 'Quelepa', 'San Antonio', 'San Gerardo', 'San Jorge', 'San Luis de la Reina', 'San Rafael Oriente', 'Sesori', 'Uluazapa'],
    'san_salvador': ['San Salvador', 'Aguilares', 'Apopa', 'Ayutuxtepeque', 'Cuscatancingo', 'Delgado', 'El Paisnal', 'Guazapa', 'Ilopango', 'Mejicanos', 'Nejapa', 'Panchimalco', 'Rosario de Mora', 'San Marcos', 'San Martín', 'Santiago Texacuangos', 'Santo Tomás', 'Soyapango', 'Tonacatepeque'],
    'san_vicente': ['San Vicente', 'Apastepeque', 'Guadalupe', 'San Cayetano Istepeque', 'San Esteban Catarina', 'San Ildefonso', 'San Lorenzo', 'San Sebastián', 'Santa Clara', 'Santo Domingo', 'Tecoluca', 'Tepetitán', 'Verapaz'],
    'santa_ana': ['Santa Ana', 'Candelaria de la Frontera', 'Chalchuapa', 'Coatepeque', 'El Congo', 'El Porvenir', 'Masahuat', 'Metapán', 'San Antonio Pajonal', 'San Sebastián Salitrillo', 'Santa Rosa Guachipilín', 'Santiago de la Frontera', 'Texistepeque'],
    'sonsonate': ['Sonsonate', 'Acajutla', 'Armenia', 'Caluco', 'Cuisnahuat', 'Izalco', 'Juayúa', 'Nahuizalco', 'Nahulingo', 'Salcoatitán', 'San Antonio del Monte', 'San Julián', 'Santa Catarina Masahuat', 'Santa Isabel Ishuatán', 'Santo Domingo de Guzmán', 'Sonzacate'],
    'usulutan': ['Usulután', 'Alegría', 'Berlín', 'California', 'Concepción Batres', 'El Triunfo', 'Ereguayquín', 'Estanzuelas', 'Jiquilisco', 'Jucuapa', 'Jucuarán', 'Mercedes Umaña', 'Nueva Granada', 'Ozatlán', 'Puerto El Triunfo', 'San Agustín', 'San Buenaventura', 'San Dionisio', 'San Francisco Javier', 'Santa Elena', 'Santa María', 'Santiago de María', 'Tecapán'],
}

TIPOS_EMPLEO = [
    ('tiempo_completo', 'Tiempo Completo'),
    ('medio_tiempo', 'Medio Tiempo'),
    ('freelance', 'Freelance/Independiente'),
    ('practicas', 'Prácticas/Pasantías'),
    ('temporal', 'Temporal/Por Proyecto'),
]

SECTORES_INDUSTRIA = [
    ('tecnologia', 'Tecnología e Informática'),
    ('construccion', 'Construcción e Ingeniería'),
    ('comercio', 'Comercio y Ventas'),
    ('restaurante', 'Restaurantes y Alimentos'),
    ('servicios', 'Servicios Profesionales'),
    ('manufactura', 'Manufactura e Industria'),
    ('agricultura', 'Agricultura y Ganadería'),
    ('educacion', 'Educación y Capacitación'),
    ('salud', 'Salud y Medicina'),
    ('transporte', 'Transporte y Logística'),
    ('turismo', 'Turismo y Hotelería'),
    ('finanzas', 'Finanzas y Banca'),
    ('marketing', 'Marketing y Publicidad'),
    ('recursos_humanos', 'Recursos Humanos'),
    ('legal', 'Legal y Jurídico'),
    ('arte', 'Arte y Diseño'),
    ('otro', 'Otro'),
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
    departamento = models.CharField(
        max_length=50,
        choices=DEPARTAMENTOS_EL_SALVADOR,
        blank=True,
        verbose_name='Departamento'
    )
    municipio = models.CharField(max_length=100, blank=True, verbose_name='Municipio')
    direccion = models.TextField(blank=True, verbose_name='Dirección')
    
    # Información profesional
    profesion = models.CharField(max_length=200, blank=True, verbose_name='Profesión u Oficio')
    biografia = models.TextField(blank=True, verbose_name='Sobre mí')
    habilidades = models.TextField(
        blank=True,
        verbose_name='Habilidades',
        help_text='Separa tus habilidades con comas. Ej: Python, Django, SQL'
    )
    
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
    institucion_educativa = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Institución Educativa'
    )
    
    # Archivos
    cv = models.FileField(upload_to='cvs/', blank=True, null=True, verbose_name='CV (PDF)')
    foto_perfil = models.ImageField(
        upload_to='fotos_perfil/candidatos/',
        blank=True,
        null=True,
        verbose_name='Foto de Perfil'
    )
    
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
    
    salario_esperado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Salario Esperado (USD)'
    )
    
    # Metadata
    perfil_completo = models.BooleanField(default=False, verbose_name='Perfil Completo')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Perfil de Candidato'
        verbose_name_plural = 'Perfiles de Candidatos'
        ordering = ['-fecha_actualizacion']
    
    def __str__(self):
        return f"Perfil de {self.usuario.get_full_name() or self.usuario.username}"
    
    def get_habilidades_lista(self):
        """Devuelve las habilidades como lista"""
        if self.habilidades:
            return [h.strip() for h in self.habilidades.split(',')]
        return []
    
    def verificar_completitud(self):
        """Verifica si el perfil está completo"""
        campos_requeridos = [
            self.telefono,
            self.departamento,
            self.profesion,
            self.biografia,
            self.habilidades,
        ]
        self.perfil_completo = all(campos_requeridos)
        self.save()
        return self.perfil_completo


# ============================================
# MODELO: EXPERIENCIA LABORAL
# ============================================

class ExperienciaLaboral(models.Model):
    """
    Modelo para registrar las experiencias laborales de un candidato.
    Relación: Un candidato puede tener múltiples experiencias.
    """
    perfil_candidato = models.ForeignKey(
        PerfilCandidato,
        on_delete=models.CASCADE,
        related_name='experiencias',
        verbose_name='Perfil del Candidato'
    )
    
    # Información del puesto
    titulo_cargo = models.CharField(
        max_length=200,
        verbose_name='Título del Cargo',
        help_text='Ej: Desarrollador Full Stack, Gerente de Ventas'
    )
    empresa = models.CharField(
        max_length=200,
        verbose_name='Empresa/Compañía'
    )
    tipo_empleo = models.CharField(
        max_length=50,
        choices=TIPOS_EMPLEO,
        default='tiempo_completo',
        verbose_name='Tipo de Empleo'
    )
    sector_industria = models.CharField(
        max_length=50,
        choices=SECTORES_INDUSTRIA,
        blank=True,
        verbose_name='Sector/Industria'
    )
    
    # Ubicación
    ubicacion = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Ubicación',
        help_text='Ciudad, País. Ej: San Salvador, El Salvador'
    )
    
    # Fechas
    fecha_inicio = models.DateField(verbose_name='Fecha de Inicio')
    fecha_fin = models.DateField(
        blank=True,
        null=True,
        verbose_name='Fecha de Finalización'
    )
    trabajo_actual = models.BooleanField(
        default=False,
        verbose_name='Trabajo Actual',
        help_text='Marca si actualmente trabajas aquí'
    )
    
    # Descripción
    descripcion = models.TextField(
        verbose_name='Descripción del Puesto',
        help_text='Describe tus responsabilidades, logros y actividades principales'
    )
    
    # Metadata
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Experiencia Laboral'
        verbose_name_plural = 'Experiencias Laborales'
        ordering = ['-trabajo_actual', '-fecha_inicio']  # Trabajo actual primero, luego por fecha
    
    def __str__(self):
        return f"{self.titulo_cargo} en {self.empresa}"
    
    def duracion(self):
        """Calcula la duración del empleo"""
        from datetime import date
        fecha_fin = self.fecha_fin if self.fecha_fin else date.today()
        delta = fecha_fin - self.fecha_inicio
        
        años = delta.days // 365
        meses = (delta.days % 365) // 30
        
        if años > 0 and meses > 0:
            return f"{años} año{'s' if años > 1 else ''} y {meses} mes{'es' if meses > 1 else ''}"
        elif años > 0:
            return f"{años} año{'s' if años > 1 else ''}"
        elif meses > 0:
            return f"{meses} mes{'es' if meses > 1 else ''}"
        else:
            return "Menos de 1 mes"
    
    def clean(self):
        """Validaciones personalizadas"""
        from django.core.exceptions import ValidationError
        
        # Si es trabajo actual, no debe tener fecha de fin
        if self.trabajo_actual and self.fecha_fin:
            raise ValidationError('Un trabajo actual no puede tener fecha de finalización.')
        
        # Si no es trabajo actual, debe tener fecha de fin
        if not self.trabajo_actual and not self.fecha_fin:
            raise ValidationError('Debes especificar la fecha de finalización o marcar como trabajo actual.')
        
        # La fecha de fin no puede ser anterior a la fecha de inicio
        if self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            raise ValidationError('La fecha de finalización no puede ser anterior a la fecha de inicio.')


# ============================================
# MODELO: PERFIL EMPRESA
# ============================================

class PerfilEmpresa(models.Model):
    """
    Perfil extendido para empresas y MYPEs. Se crea automáticamente al registrarse.
    """
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='perfil_empresa',
        verbose_name='Usuario'
    )
    
    # Información básica
    nombre_empresa = models.CharField(max_length=200, verbose_name='Nombre de la Empresa')
    tipo_empresa = models.CharField(
        max_length=50,
        choices=[
            ('formal', 'Empresa Formal Registrada'),
            ('mype', 'Microempresa o Pequeña Empresa (MYPE)'),
            ('mype_informal', 'MYPE Informal (En proceso de formalización)'),
        ],
        default='mype',
        verbose_name='Tipo de Empresa'
    )
    rubro = models.CharField(max_length=50, choices=RUBROS_EMPRESA, blank=True, verbose_name='Rubro')
    descripcion = models.TextField(blank=True, verbose_name='Descripción de la Empresa')
    
    # Misión y Visión
    mision = models.TextField(blank=True, verbose_name='Misión', help_text='¿Cuál es el propósito de tu empresa?')
    vision = models.TextField(blank=True, verbose_name='Visión', help_text='¿Hacia dónde se dirige tu empresa?')
    
    # Ubicación
    departamento = models.CharField(
        max_length=50,
        choices=DEPARTAMENTOS_EL_SALVADOR,
        blank=True,
        verbose_name='Departamento'
    )
    municipio = models.CharField(max_length=100, blank=True, verbose_name='Municipio')
    direccion = models.TextField(blank=True, verbose_name='Dirección')
    
    # Contacto
    telefono_contacto = models.CharField(max_length=15, blank=True, verbose_name='Teléfono')
    correo_contacto = models.EmailField(blank=True, verbose_name='Correo de Contacto')
    sitio_web = models.URLField(blank=True, verbose_name='Sitio Web')
    
    # Redes Sociales
    facebook = models.URLField(blank=True, verbose_name='Facebook', help_text='URL completa de Facebook')
    instagram = models.URLField(blank=True, verbose_name='Instagram', help_text='URL completa de Instagram')
    linkedin = models.URLField(blank=True, verbose_name='LinkedIn', help_text='URL completa de LinkedIn')
    twitter = models.URLField(blank=True, verbose_name='Twitter/X', help_text='URL completa de Twitter')
    
    # Información legal
    numero_registro = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Número de Registro/NIT'
    )
    documento_verificacion = models.FileField(
        upload_to='documentos_empresas/',
        blank=True,
        null=True,
        verbose_name='Documento de Verificación'
    )
    
    # Logo
    logo = models.ImageField(
        upload_to='logos_empresas/',
        blank=True,
        null=True,
        verbose_name='Logo'
    )
    
    # Verificación (tick azul)
    es_verificada = models.BooleanField(default=False, verbose_name='Empresa Verificada ✓')
    fecha_verificacion = models.DateTimeField(blank=True, null=True)
    
    # Info adicional
    cantidad_empleados = models.CharField(
        max_length=50,
        choices=[
            ('1-5', '1-5 empleados'),
            ('6-10', '6-10 empleados'),
            ('11-25', '11-25 empleados'),
            ('26-50', '26-50 empleados'),
            ('51-100', '51-100 empleados'),
            ('100+', 'Más de 100 empleados'),
        ],
        blank=True,
        verbose_name='Cantidad de Empleados'
    )
    año_fundacion = models.IntegerField(blank=True, null=True, verbose_name='Año de Fundación')
    
    # Estado
    perfil_completo = models.BooleanField(default=False)
    activa = models.BooleanField(default=True, verbose_name='Empresa Activa')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Perfil de Empresa'
        verbose_name_plural = 'Perfiles de Empresas'
        ordering = ['-fecha_actualizacion']
    
    def __str__(self):
        return self.nombre_empresa or f"Empresa de {self.usuario.username }"
    
    def verificar_completitud(self):
        """Verifica si el perfil está completo"""
        campos_requeridos = [
            self.nombre_empresa,
            self.rubro,
            self.descripcion,
            self.departamento,
            self.telefono_contacto,
            self.correo_contacto,
        ]
        self.perfil_completo = all(campos_requeridos)
        self.save()
        return self.perfil_completo


# ============================================
# SEÑALES: Auto-crear perfiles al registrarse
# ============================================

@receiver(post_save, sender=Usuario)
def crear_perfil_automatico(sender, instance, created, **kwargs):
    """
    Cuando se crea un Usuario, se crea automáticamente su perfil según su rol
    """
    if created:
        if instance.rol == 'candidato':
            PerfilCandidato.objects.create(usuario=instance)
        elif instance.rol == 'empresa':
            PerfilEmpresa.objects.create(
                usuario=instance,
                nombre_empresa=instance.first_name or 'Mi Empresa'
            )
