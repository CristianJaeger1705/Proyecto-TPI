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
    user = os.getenv('EMAIL_HOST_USER', 'NO DEFINIDO')
    pwd = os.getenv('EMAIL_HOST_PASSWORD', '')
    
    longitud = len(pwd)
    primer_caracter = pwd[0] if pwd else 'N/A'
    ultimo_caracter = pwd[-1] if pwd else 'N/A'
    
    return HttpResponse(f"""
        <h1>Diagnóstico Rápido</h1>
        <p><strong>Usuario:</strong> {user}</p>
        <p><strong>Longitud contraseña:</strong> {longitud}</p>
        <p><strong>Primer caracter:</strong> {primer_caracter}</p>
        <p><strong>Último caracter:</strong> {ultimo_caracter}</p>
        <p>🚀 Render responde sin timeout.</p>
    """)
