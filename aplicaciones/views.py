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

def test_brevo(request):
    try:
        send_mail(
            subject="Prueba Brevo OK",
            message="Este correo fue enviado correctamente desde Brevo 😎",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["tu-correo@gmail.com"],
            fail_silently=False,
        )
        return HttpResponse("<h1>✔️ Enviado correctamente</h1>")
    except Exception as e:
        return HttpResponse(f"<h1>❌ Error: {e}</h1>")
    

def debug_smtp(request):
    return HttpResponse(f"""
        USER = {os.getenv("EMAIL_HOST_USER")}
        PASS_LEN = {len(os.getenv("EMAIL_HOST_PASSWORD") or '')}
    """)