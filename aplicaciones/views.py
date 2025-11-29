from django.shortcuts import render

def hola_mundo(request):
    return render(request, 'hola_mundo.html')

from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
import os

def prueba_email(request):
    # 1. Verificar credenciales visualmente
    user = os.getenv('EMAIL_HOST_USER')
    pwd = os.getenv('EMAIL_HOST_PASSWORD')
    
    debug_info = f"""
    <h1>Diagnóstico de Correo</h1>
    <p><strong>Usuario:</strong> {user}</p>
    <p><strong>Contraseña configurada:</strong> {'SÍ' if pwd else 'NO'} (Longitud: {len(str(pwd))})</p>
    <p><strong>Backend:</strong> {settings.EMAIL_BACKEND}</p>
    <p><strong>Host:</strong> {settings.EMAIL_HOST}:{settings.EMAIL_PORT}</p>
    <p><strong>TLS/SSL:</strong> TLS={settings.EMAIL_USE_TLS} / SSL={settings.EMAIL_USE_SSL}</p>
    <hr>
    """
    
    try:
        # 2. Intentar enviar
        send_mail(
            'Prueba Definitiva Render',
            'Si lees esto, funcionó. Ya puedes dormir tranquilo.',
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER], # Se envía a ti mismo
            fail_silently=False,
        )
        return HttpResponse(debug_info + "<h2 style='color:green'>✅ ¡ÉXITO! Correo enviado. Revisa tu bandeja.</h2>")
    except Exception as e:
        return HttpResponse(debug_info + f"<h2 style='color:red'>❌ ERROR: {e}</h2>")