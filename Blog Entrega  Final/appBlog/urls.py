from django.urls import path
from .views import *

urlpatterns = [
    # Index
    path('', index, name='index'),
    
    # About
    path('about/', about, name='about'),
    
    # Encontrar Publicacion
    path('buscar/', encontrarPublicacion, name='encontrar_publicacion'),

    # Publicaciones
    path('publicacion/lista/', PublicacionListView.as_view(), name='publicacion_lista'),
    path('publicacion/<int:pk>/', PublicacionDetailView.as_view(), name='publicacion_detalle'),
    path('publicacion/nuevo/', PublicacionCreateView.as_view(), name='publicacion_crear'),
    path('publicacion/editar/<int:pk>/', PublicacionUpdateView.as_view(), name='publicacion_editar'),
    path('publicacion/eliminar/<int:pk>/', PublicacionDeleteView.as_view(), name='publicacion_eliminar'),
    
    # Comentarios 'publicacion_pk y comentario_pk para el contexto especifico'
    path('publicacion/<int:publicacion_pk>/comentario/nuevo/', ComentarioCreateView.as_view(), name='comentario_crear'),
    path('publicacion/<int:publicacion_pk>/comentario/lista/', ComentarioListView.as_view(), name='comentario_lista'),
    path('publicacion/<int:publicacion_pk>/comentario/editar/<int:comentario_pk>', ComentarioUpdateView.as_view(), name='comentario_editar'),
    path('publicacion/<int:publicacion_pk>/comentario/eliminar/<int:comentario_pk>', ComentarioDeleteView.as_view(), name='comentario_eliminar'),
    
    # Categorias
    path('categoria/lista/', CategoriaListView.as_view(), name='categoria_lista'),
    path('categoria/nuevo/', CategoriaCreateView.as_view(), name='categoria_crear'),
    path('categoria/editar/<int:pk>', CategoriaUpdateView.as_view(), name='categoria_editar'),
    path('categoria/eliminar/<int:pk>', CategoriaDeleteView.as_view(), name='categoria_eliminar'),
    
    # Eventos
    path('evento/lista/', EventoListView.as_view(), name='evento_lista'),
    path('evento/<int:pk>/', EventoDetailView.as_view(), name='evento_detalle'),
    path('evento/nuevo/', EventoCreateView.as_view(), name='evento_crear'),
    path('evento/editar/<int:pk>/', EventoUpdateView.as_view(), name='evento_editar'),
    path('evento/eliminar/<int:pk>/', EventoDeleteView.as_view(), name='evento_eliminar'),
    
    # Login, Logout, Registration
    path('login/', login_request , name = 'login'),
    path('logout/', user_logout , name = 'logout'),
    path('registrar/', register , name = 'registro'),
    
    # Editar Perfil, Cambiar clave, Avatar
    path('perfil/', editProfile , name = 'perfil'),
    path('password/', CambiarClave.as_view(), name = 'cambiar_clave'),
    path('agregar_avatar/', agregarAvatar , name = 'agregar_avatar'),
]
