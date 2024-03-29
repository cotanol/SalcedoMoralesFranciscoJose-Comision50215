from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

# El atributo widgets de la class Meta para ponerle una clase y estilizar con css

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        fields = ['titulo', 'contenido', 'categorias', 'imagen']
        widgets = {
            'categorias': forms.SelectMultiple(attrs={'class': 'widget-categorias'}),
            'contenido': forms.Textarea(attrs={'class': 'background-white'}),
            'titulo': forms.TextInput(attrs={'class': 'background-white'}),
        }
        
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'background-white'})
        }
        
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'background-white'}),
            'descripcion': forms.Textarea(attrs={'class': 'background-white'}),
        }
        
class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'descripcion', 'fecha_evento', 'lugar', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'background-white'}),
            'descripcion': forms.Textarea(attrs={'class': 'background-white'}),
            'fecha_evento': forms.DateTimeInput(attrs={'class': 'background-white', 'type': 'datetime-local'}),
            'lugar': forms.TextInput(attrs={'class': 'background-white'}),
        }
        
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirma Contraseña', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class UserEditForm(UserChangeForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label='Nombre/s', max_length=50, required=True)
    last_name = forms.CharField(label='Apellido/s', max_length=50, required=True)
    password = None
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        
class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['imagen']
        