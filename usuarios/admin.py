from django.contrib import admin
from django.utils.html import format_html
from .models import Usuario, PerfilCandidato, PerfilEmpresa, ExperienciaLaboral


@admin.register(PerfilCandidato)
class PerfilCandidatoAdmin(admin.ModelAdmin):
    """Panel de administración para Perfiles de Candidatos"""
    list_display = ['usuario_nombre', 'profesion', 'departamento', 'tiene_cv', 'perfil_completo']
    list_filter = ['perfil_completo', 'departamento', 'nivel_educacion']
    search_fields = ['usuario__username', 'usuario__email', 'profesion', 'habilidades']
    
    def usuario_nombre(self, obj):
        return obj.usuario.get_full_name() or obj.usuario.username
    usuario_nombre.short_description = 'Candidato'
    
    def tiene_cv(self, obj):
        if obj.cv:
            return format_html('<span style="color: green;">✓ Sí</span>')
        return format_html('<span style="color: red;">✗ No</span>')
    tiene_cv.short_description = 'CV'


@admin.register(PerfilEmpresa)
class PerfilEmpresaAdmin(admin.ModelAdmin):
    """Panel de administración para Perfiles de Empresas - Vista de Soporte/Verificación"""
    list_display = ['nombre_empresa', 'tipo_empresa', 'cantidad_empleados', 'rubro', 'departamento', 'verificada_badge', 'perfil_completo']
    list_filter = ['es_verificada', 'activa', 'tipo_empresa', 'rubro', 'departamento', 'cantidad_empleados', 'perfil_completo']
    search_fields = ['nombre_empresa', 'usuario__username', 'usuario__email', 'numero_registro']
    readonly_fields = ['fecha_verificacion', 'fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('usuario', 'nombre_empresa', 'tipo_empresa', 'rubro', 'descripcion', 'logo')
        }),
        ('Misión y Visión', {
            'fields': ('mision', 'vision'),
            'classes': ('collapse',)
        }),
        ('Ubicación', {
            'fields': ('departamento', 'municipio', 'direccion')
        }),
        ('Contacto', {
            'fields': ('telefono_contacto', 'correo_contacto', 'sitio_web')
        }),
        ('Redes Sociales', {
            'fields': ('facebook', 'instagram', 'linkedin', 'twitter'),
            'classes': ('collapse',)
        }),
        ('Información Legal y Verificación', {
            'fields': ('numero_registro', 'documento_verificacion', 'es_verificada', 'fecha_verificacion'),
            'classes': ('wide',)
        }),
        ('Información Administrativa', {
            'fields': ('cantidad_empleados', 'año_fundacion', 'activa', 'perfil_completo'),
            'description': 'Información visible solo para administradores'
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['verificar_empresa', 'desverificar_empresa']
    
    def verificada_badge(self, obj):
        if obj.es_verificada:
            return format_html('<span style="color: #1DA1F2; font-weight: bold;">✓ Verificada</span>')
        return format_html('<span style="color: gray;">Sin verificar</span>')
    verificada_badge.short_description = 'Estado de Verificación'
    
    def verificar_empresa(self, request, queryset):
        from django.utils import timezone
        count = queryset.update(es_verificada=True, fecha_verificacion=timezone.now())
        self.message_user(request, f'{count} empresa(s) verificada(s) exitosamente.')
    verificar_empresa.short_description = '✓ Verificar empresa seleccionada'
    
    def desverificar_empresa(self, request, queryset):
        count = queryset.update(es_verificada=False, fecha_verificacion=None)
        self.message_user(request, f'{count} empresa(s) desverificada(s).')
    desverificar_empresa.short_description = '✗ Quitar verificación'


@admin.register(ExperienciaLaboral)
class ExperienciaLaboralAdmin(admin.ModelAdmin):
    """Panel de administración para Experiencias Laborales"""
    list_display = ['candidato_nombre', 'titulo_cargo', 'empresa', 'tipo_empleo', 'trabajo_actual', 'fecha_inicio', 'fecha_fin']
    list_filter = ['trabajo_actual', 'tipo_empleo', 'sector_industria']
    search_fields = ['perfil_candidato__usuario__username', 'titulo_cargo', 'empresa', 'descripcion']
    date_hierarchy = 'fecha_inicio'
    
    def candidato_nombre(self, obj):
        return obj.perfil_candidato.usuario.get_full_name() or obj.perfil_candidato.usuario.username
    candidato_nombre.short_description = 'Candidato'
