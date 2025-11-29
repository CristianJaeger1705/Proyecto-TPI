from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notificacion

@login_required
def api_nuevas(request):
    usuario = request.user
    # Usar fecha_envio en lugar de fecha_creacion
    mensajes = Mensaje.objects.filter(conversacion__participantes=usuario).order_by('fecha_envio')
    
    data = [
        {
            'usuario': m.remitente.username,
            'mensaje': m.texto,
            'fecha': m.fecha_envio.strftime("%Y-%m-%d %H:%M:%S")
        }
        for m in mensajes
    ]
    return JsonResponse(data, safe=False)