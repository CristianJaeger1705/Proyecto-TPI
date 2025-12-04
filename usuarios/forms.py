from django import forms
from django.contrib.auth.models import User
from perfiles.models import PerfilCandidato, PerfilEmpresa, ExperienciaLaboral
from django import forms
from . models import Review

class FormularioPerfilCandidato(forms.ModelForm):
    """
    Formulario para que los candidatos completen su perfil
    """
    class Meta:
        model = PerfilCandidato
        fields = [
            'telefono',
            'fecha_nacimiento',
            'departamento',
            'municipio',
            'direccion',
            'profesion',
            'biografia',
            'habilidades',
            'nivel_educacion',
            'institucion_educativa',
            'foto_perfil',
            'cv',
            'disponibilidad',
            'salario_esperado',
        ]
        widgets = {
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '7123-4567'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'departamento': forms.Select(attrs={
                'class': 'form-control'
            }),
            'municipio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: San Salvador'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Dirección completa'
            }),
            'profesion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Desarrollador Web, Mecánico, Contador'
            }),
            'biografia': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Cuéntanos sobre ti, tu experiencia y qué te hace destacar...'
            }),
            'habilidades': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ej: Python, Django, JavaScript, Trabajo en equipo, etc.'
            }),
            'experiencia_laboral': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe tu experiencia laboral previa...'
            }),
            'nivel_educacion': forms.Select(attrs={
                'class': 'form-control'
            }),
            'institucion_educativa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Universidad de El Salvador'
            }),
            'foto_perfil': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'cv': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'disponibilidad': forms.Select(attrs={
                'class': 'form-control'
            }),
            'salario_esperado': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '500.00',
                'step': '0.01'
            }),
        }
        labels = {
            'telefono': 'Teléfono de Contacto',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'departamento': 'Departamento',
            'municipio': 'Municipio',
            'direccion': 'Dirección',
            'profesion': 'Profesión u Oficio',
            'biografia': 'Sobre ti',
            'habilidades': 'Habilidades (separadas por comas)',
            'experiencia_laboral': 'Experiencia Laboral',
            'nivel_educacion': 'Nivel de Educación',
            'institucion_educativa': 'Institución Educativa',
            'foto_perfil': 'Foto de Perfil',
            'cv': 'Curriculum Vitae (CV)',
            'disponibilidad': 'Disponibilidad',
            'salario_esperado': 'Salario Esperado Mensual (USD)',
        }


class FormularioPerfilEmpresa(forms.ModelForm):
    """
    Formulario para que las empresas completen su perfil
    """
    class Meta:
        model = PerfilEmpresa
        fields = [
            'nombre_empresa',
            'tipo_empresa',
            'rubro',
            'descripcion',
            'mision',
            'vision',
            'departamento',
            'municipio',
            'direccion',
            'telefono_contacto',
            'correo_contacto',
            'sitio_web',
            'facebook',
            'instagram',
            'linkedin',
            'twitter',
            'numero_registro',
            'logo',
            'cantidad_empleados',
            'año_fundacion',
        ]
        widgets = {
            'nombre_empresa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de tu empresa o negocio'
            }),
            'tipo_empresa': forms.Select(attrs={
                'class': 'form-control'
            }),
            'rubro': forms.Select(attrs={
                'class': 'form-control'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe a qué se dedica tu empresa...'
            }),
            'mision': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '¿Cuál es el propósito de tu empresa?'
            }),
            'vision': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '¿Hacia dónde se dirige tu empresa?'
            }),
            'departamento': forms.Select(attrs={
                'class': 'form-control'
            }),
            'municipio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: San Salvador'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Dirección completa de la empresa'
            }),
            'telefono_contacto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '2222-2222 o 7123-4567'
            }),
            'correo_contacto': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'contacto@empresa.com'
            }),
            'sitio_web': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.tuempresa.com (opcional)'
            }),
            'facebook': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://facebook.com/tuempresa'
            }),
            'instagram': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://instagram.com/tuempresa'
            }),
            'linkedin': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/company/tuempresa'
            }),
            'twitter': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://twitter.com/tuempresa'
            }),
            'numero_registro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'NIT o Número de Registro (opcional para MYPEs)'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'cantidad_empleados': forms.Select(attrs={
                'class': 'form-control'
            }),
            'año_fundacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '2020',
                'min': '1900',
                'max': '2030'
            }),
        }
        labels = {
            'nombre_empresa': 'Nombre de la Empresa',
            'tipo_empresa': 'Tipo de Empresa',
            'rubro': 'Rubro o Sector',
            'descripcion': 'Descripción de la Empresa',
            'mision': 'Misión',
            'vision': 'Visión',
            'departamento': 'Departamento',
            'municipio': 'Municipio',
            'direccion': 'Dirección',
            'telefono_contacto': 'Teléfono de Contacto',
            'correo_contacto': 'Correo Electrónico',
            'sitio_web': 'Sitio Web',
            'facebook': 'Facebook',
            'instagram': 'Instagram',
            'linkedin': 'LinkedIn',
            'twitter': 'Twitter / X',
            'numero_registro': 'NIT / Número de Registro',
            'logo': 'Logo de la Empresa',
            'cantidad_empleados': 'Cantidad de Empleados',
            'año_fundacion': 'Año de Fundación',
        }


class FormularioExperienciaLaboral(forms.ModelForm):
    """
    Formulario para agregar/editar experiencias laborales de un candidato
    """
    class Meta:
        model = ExperienciaLaboral
        fields = [
            'titulo_cargo',
            'empresa',
            'tipo_empleo',
            'sector_industria',
            'ubicacion',
            'fecha_inicio',
            'fecha_fin',
            'trabajo_actual',
            'descripcion',
        ]
        widgets = {
            'titulo_cargo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Desarrollador Full Stack'
            }),
            'empresa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Tech Solutions SV'
            }),
            'tipo_empleo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'sector_industria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'ubicacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: San Salvador, El Salvador'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'trabajo_actual': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe tus responsabilidades, logros y actividades principales...'
            }),
        }
        labels = {
            'titulo_cargo': 'Título del Cargo',
            'empresa': 'Empresa/Compañía',
            'tipo_empleo': 'Tipo de Empleo',
            'sector_industria': 'Sector/Industria',
            'ubicacion': 'Ubicación (Ciudad, País)',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin': 'Fecha de Finalización',
            'trabajo_actual': '¿Trabajo actual?',
            'descripcion': 'Descripción del Puesto',
        }
        help_texts = {
            'trabajo_actual': 'Marca esta casilla si actualmente trabajas aquí',
            'fecha_fin': 'Deja en blanco si es tu trabajo actual',
        }

class ReviewForm(forms.ModelForm):
    calificacion = forms.ChoiceField(
        choices=[(i, f"{i} estrellas") for i in range(1, 6)],
        widget=forms.RadioSelect
    )

    class Meta:
        model = Review
        fields = ['calificacion', 'comentario']
