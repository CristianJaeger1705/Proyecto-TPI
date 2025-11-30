# Proyecto TPI - LaburoSV

Plataforma de búsqueda de empleos, desarrollado con Django.

## Requisitos Previos

- Python 3.10+
- `pip` (manejador de paquetes de Python)
- `virtualenv` (para crear entornos virtuales)
- PostgreSQL (o la base de datos que desees configurar)

## Instalación

Sigue estos pasos para configurar el entorno de desarrollo local.

1.  **Clona el repositorio:**

    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd proyecto-tpi
    ```

2.  **Crea y activa un entorno virtual:**

    ```bash
    python -m venv venv
    source venv/bin/activate
    # En Windows, usa: venv\Scripts\activate
    ```

3.  **Instala las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura las variables de entorno:**
    Crea un archivo llamado `.env` en la raíz del proyecto. Copia y pega el siguiente contenido, reemplazando los valores según tu configuración local.

    ```ini
    # .env

    # Django Core
    # Reemplaza 'secret-key-aqui' con una clave secreta real y única.
    SECRET_KEY='secret-key-aqui'
    DEBUG=True

    # Configuración de la Base de Datos (PostgreSQL)
    DB_NAME='nombre_de_tu_db'
    DB_USER='usuario_de_tu_db'
    DB_PASSWORD='password_de_tu_db'
    DB_HOST='localhost'
    DB_PORT='5432'

    # Configuración de Email (Gmail)
    # IMPORTANTE: Usa una contraseña de aplicación si tienes 2FA activado.
    EMAIL_HOST_USER='tu_correo@gmail.com'
    EMAIL_HOST_PASSWORD='tu_contraseña_de_aplicacion'
    EMAIL_HOST_USER='user_brevo'
    EMAIL_HOST_PASSWORD='contraseña_brevo'
    DEFAULT_FROM_EMAIL='correo_from'
    GOOGLE_CLIENT_ID='cliente_id'
    GOOGLE_CLIENT_SECRET='cliente_secreto'
    ```

5.  **Aplica las migraciones de la base de datos:**
    Asegúrate de que tu servidor de base de datos esté corriendo antes de ejecutar este comando.

    ```bash
    python manage.py migrate
    ```

6.  **Crea un superusuario:**
    Esto te permitirá acceder al panel de administración de Django (`/admin`).
    ```bash
    python manage.py createsuperuser
    ```

## Ejecución

Para iniciar el servidor de desarrollo, ejecuta:

```bash
python manage.py runserver
```

El sitio estará disponible en `http://127.0.0.1:8000`.
