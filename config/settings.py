"""
Django settings for config project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# VARIABLES BÁSICAS
# =========================
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    'laburosv.com',
    'proyecto-tpi-jtgf.onrender.com',
    'localhost',
    '127.0.0.1'
]

# =========================
# APPS
# =========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'mensajeria.apps.MensajeriaConfig',


    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'usuarios',
    'ofertas',
    'perfiles',
    'postulaciones',
    
    'adminpanel',
    'core',

    'channels',

    # Cloudinary solo se activará en producción
    'cloudinary',
    'cloudinary_storage',
]

# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# =========================
# TEMPLATES
# =========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

# =========================
# CHANNELS (Redis opcional)
# =========================
REDIS_URL = os.getenv("REDIS_URL", None)

if REDIS_URL:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {"hosts": [REDIS_URL]},
        },
    }
else:
    CHANNEL_LAYERS = {
        "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}
    }

# =========================
# DATABASE LOCAL POR DEFECTO
# =========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'ProyectoTPI'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'admin'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# =========================
# PRODUCCIÓN (Render)
# =========================
if os.getenv("RENDER") == "true":
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )

# =========================
# VALIDACIÓN CONTRASEÑAS
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =========================
# INTERNACIONALIZACIÓN
# =========================
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/El_Salvador'
USE_I18N = True
USE_TZ = True

# =========================
# ARCHIVOS ESTÁTICOS
# =========================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# =========================
# ARCHIVOS MEDIA (LOCAL)
# =========================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =========================
# STORAGE: CLOUDINARY SOLO EN PRODUCCIÓN
# =========================
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'  
CLOUDINARY_STORAGE = {
        "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
        "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
        "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
    }
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Whitenoise solo para estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =========================
# USUARIO PERSONALIZADO
# =========================
AUTH_USER_MODEL = 'usuarios.Usuario'

# =========================
# MENSAJERÍA
# =========================
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# =========================
# LOGIN
# =========================
LOGIN_URL = 'usuarios:login'
LOGIN_REDIRECT_URL = 'pagina_principal'
LOGOUT_REDIRECT_URL = 'pagina_principal'

# =========================
# EMAIL
# =========================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp-relay.brevo.com"
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

# =========================
# ALLAUTH
# =========================
SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_ADAPTER = "usuarios.adapters.GoogleAccountAdapter"

ACCOUNT_SIGNUP_FIELDS = ['email', 'username', 'password1', 'password2']
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGIN_METHODS = {"username"}
SOCIALACCOUNT_LOGIN_ON_GET = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv("GOOGLE_CLIENT_ID"),
            'secret': os.getenv("GOOGLE_CLIENT_SECRET"),
            'key': ''
        }
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
