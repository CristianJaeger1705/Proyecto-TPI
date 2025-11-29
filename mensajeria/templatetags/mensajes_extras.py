from django import template

register = template.Library()

@register.filter
def mensajes_no_leidos(grupo, user):
    return grupo.mensajes.exclude(remitente=user).count()
