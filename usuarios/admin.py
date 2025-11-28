# apps/empresas/admin.py
from django.contrib import admin
from django.core.mail import send_mail
from .models import SolicitudEmpresa
from django.conf import settings

@admin.register(SolicitudEmpresa)
class SolicitudEmpresaAdmin(admin.ModelAdmin):
    list_display = ("nombre_empresa", "correo", "estado")
    actions = ["aprobar_solicitud"]

    def aprobar_solicitud(self, request, queryset):
        for s in queryset:
            s.estado = "aprobada"
            s.save()

            link = f"http://127.0.0.1:8000/usuarios/registrar_empresa/{s.token}/"

            send_mail(
                subject="Solicitud aprobada – Crear cuenta",
                message=f"Su solicitud fue aprobada. Cree su cuenta aquí: {link}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[s.correo],
            )

        self.message_user(request, "Solicitudes aprobadas y correos enviados.")
        