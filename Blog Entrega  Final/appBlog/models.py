from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True, help_text='Una breve descripcion')
    imagen = models.ImageField(upload_to='categorias', blank='True', null='True', help_text='Imagen referente a la categoria')

    def __str__(self):
        return self.nombre
    
class Publicacion(models.Model):
    titulo = models.CharField(max_length=200, unique=True)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(default=now)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    categorias = models.ManyToManyField(Categoria, related_name='publicaciones')
    imagen = models.ImageField(upload_to='publicacion', blank='True', null='True', help_text='Imagen referente a la publicacion')
    
    def __str__(self):
        return self.titulo
    
class Comentario(models.Model):
    publicacion = models.ForeignKey(Publicacion, related_name='comentarios', on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(default=now)
    
    def __str__(self):
        return f'Comentario de {self.autor} en {self.publicacion}'
    
class Evento(models.Model):
    titulo = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField()
    fecha_publicacion = models.DateTimeField(default=now)
    fecha_evento = models.DateTimeField(default=now)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    lugar = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True, help_text='Imagen referente al evento')

    def __str__(self):
        return self.titulo
    
class Avatar(models.Model):
    imagen = models.ImageField(upload_to='avatares', blank=True, null=True, help_text='Imagen referente al avatar')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user} {self.imagen}'