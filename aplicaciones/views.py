from django.shortcuts import render

def hola_mundo(request):
    return render(request, 'hola_mundo.html')

from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
import os

from django.http import HttpResponse
import os
import smtplib
import ssl

def diagnostico_correo(request):
    # 1. Leer variables
    user = os.getenv('EMAIL_HOST_USER', 'NO DEFINIDO')
    pwd = os.getenv('EMAIL_HOST_PASSWORD', '')
    
    # 2. Análisis de contraseña (SIN mostrarla, solo longitud y bordes)
    longitud = len(pwd)
    primer_caracter = pwd[0] if pwd else 'N/A'
    ultimo_caracter = pwd[-1] if pwd else 'N/A'
    
    mensaje = f"""
    <html>
        <body style='font-family: sans-serif; padding: 20px;'>
            <h1>🔍 Diagnóstico Render</h1>
            <h3>Análisis de Variables:</h3>
            <ul>
                <li><strong>Usuario:</strong> {user}</li>
                <li><strong>Longitud Contraseña:</strong> {longitud} (Debe ser 16)</li>
                <li><strong>Primer caracter:</strong> '{primer_caracter}'</li>
                <li><strong>Último caracter:</strong> '{ultimo_caracter}'</li>
            </ul>
    """
    
    # 3. Prueba de Conexión Real (SSL 465)
    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
        server.login(user, pwd)
        mensaje += "<h2 style='color:green'>✅ ÉXITO: Google aceptó la contraseña.</h2>"
        server.quit()
    except Exception as e:
        mensaje += f"<h2 style='color:red'>❌ ERROR: {e}</h2>"
        
    mensaje += "</body></html>"
    return HttpResponse(mensaje)