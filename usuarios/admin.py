
from django.contrib import admin
from django.core.mail import send_mail
from .models import SolicitudEmpresa
from django.conf import settings

# Register your models here.
@admin.register(SolicitudEmpresa)
class SolicitudEmpresaAdmin(admin.ModelAdmin):
    list_display = ("nombre_empresa", "correo", "estado")
    actions = ["aprobar_solicitud"]

    def aprobar_solicitud(self, request, queryset):
        for s in queryset:
            s.estado = "aprobada"
            s.save()

            link = f"https://laburosv.com//usuarios/registrar_empresa/{s.token}/"

            send_mail(
                subject="Solicitud aprobada – Crear cuenta",
                message=f"Su solicitud fue aprobada. Cree su cuenta aquí: {link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[s.correo],
            )

        self.message_user(request, "Solicitudes aprobadas y correos enviados.")