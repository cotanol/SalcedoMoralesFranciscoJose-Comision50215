from .models import Publicacion, Evento

# Creado porque en los sidebars no quiero que se repita los mismos que en el main en las listas.

def ultimas_publicaciones(request):
    # Obtener las últimas 4 publicaciones
    publicaciones = Publicacion.objects.order_by('-fecha_publicacion')[:4]
    return {'ultimas_publicaciones': publicaciones}

def ultimos_eventos(request):
    # Obtener los últimos 4 eventos
    eventos = Evento.objects.order_by('-fecha_evento')[:4]
    return {'ultimos_eventos': eventos}