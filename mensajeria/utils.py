from .models import Chat

def obtener_o_crear_chat_individual(usuario1, usuario2):
    """
    Devuelve el chat individual entre dos usuarios, si no existe lo crea.
    """
    chats = Chat.objects.filter(es_grupal=False, participantes=usuario1).filter(participantes=usuario2)
    if chats.exists():
        return chats.first()
    chat = Chat.objects.create(es_grupal=False)
    chat.participantes.add(usuario1, usuario2)
    chat.save()
    return chat
