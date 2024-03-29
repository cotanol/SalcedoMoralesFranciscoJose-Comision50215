from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .models import *
from .forms import *

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

# INDEX
def index(request):
    return render(request, 'bases/index.html')

# ABOUT
def about(request):
    return render(request, 'about.html')

# ENCONTRAR PUBLICACION
"""
En este caso no se creo la vista ni el html para hacer las busquedas, porque 
la busqueda se podra hacer desde cualquier pagina del proyecto.
"""
def encontrarPublicacion(request):
    if request.GET['buscar']:
        patron = request.GET['buscar']
        publicaciones = Publicacion.objects.filter(titulo__icontains=patron)
        return render(request, 'publicacion/publicacion_lista.html', {
            'publicaciones': publicaciones
        })
        
    return render(request, 'publicacion/publicacion_lista.html', {
        'libros':  Publicacion.objects.all()
    })

# PUBLICACIONES

class PublicacionListView(ListView):
    """
    paginate -> Al ser una lista queria que se mostrasen solo 5 por pagina
    context_object_name -> Para usarla variable en el template de django
    get_queryset -> Para ordenarla basado en la fecha mas actual que se publico
    """
    model = Publicacion
    context_object_name = 'publicaciones'
    template_name = 'publicacion/publicacion_lista.html'
    paginate_by = 5
    
    def get_queryset(self):
        return Publicacion.objects.all().order_by('-fecha_publicacion')
    
class PublicacionDetailView(DetailView):
    model = Publicacion
    template_name = 'publicacion/publicacion_detalle.html'
    

class PublicacionCreateView(LoginRequiredMixin, CreateView):
    # form_class -> para el formulario para el modelo en cuestion
    
    model = Publicacion
    form_class = PublicacionForm # para el formulario para el modelo en cuestion
    success_url = reverse_lazy('publicacion_lista')
    template_name = 'publicacion/publicacion_crear.html'
    
    def form_valid(self, form):
        form.instance.autor = self.request.user  # Usuario logueado como autor
        return super().form_valid(form)
    
class PublicacionUpdateView(LoginRequiredMixin, UpdateView):
    model = Publicacion
    form_class = PublicacionForm
    success_url = reverse_lazy('publicacion_lista')
    template_name = 'publicacion/publicacion_editar.html'
    
class PublicacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Publicacion
    success_url = reverse_lazy('publicacion_lista')
    template_name = 'publicacion/publicacion_eliminar.html'
    
# COMENTARIOS
class ComentarioCreateView(LoginRequiredMixin, CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentarios/comentario_crear.html'
    
    """
    form_valid:
        Se sobrescribe el método form_valid para asignar automáticamente
        el `autor` del comentario al usuario actualmente autenticado y asociar
        el comentario con la `publicacion` específica basada en `publicacion_pk`
        obtenida de los argumentos de URL.
    """
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        form.instance.publicacion_id = self.kwargs['publicacion_pk']
        return super().form_valid(form)
    
    """
    get_success_url:
        Sobrescribe el método get_success_url para redirigir al usuario
        a la lista de comentarios de la publicación específica una vez que
        el comentario se ha creado exitosamente.
    """
    def get_success_url(self):
        return reverse_lazy('comentario_lista', kwargs={'publicacion_pk': self.kwargs['publicacion_pk']})
    
class ComentarioListView(ListView):
    model = Comentario
    template_name = 'comentarios/comentario_lista.html'

    """
    get_queryset:
        Retornar solo los comentarios asociados a la publicacion, tambien hay un order_by()
        que es para que se muestren primero los comentarios mas nuevos en la lista.
    """
    def get_queryset(self):
        self.publicacion = get_object_or_404(Publicacion, pk=self.kwargs['publicacion_pk'])
        return Comentario.objects.filter(publicacion_id=self.kwargs['publicacion_pk']).order_by('-fecha_publicacion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publicacion'] = self.publicacion  # Agrega la publicación al contexto
        return context
    
class ComentarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'comentarios/comentario_editar.html'
    
    """
    Obtener el objeto Comentario especifico el cual se actualizara
    """
    def get_object(self, queryset=None):
        return get_object_or_404(Comentario, pk=self.kwargs.get('comentario_pk'))
    
    """
    publicacion_pk para asegurar que la redireccion sea al objeto correcto
    """
    def get_success_url(self):
        return reverse_lazy('comentario_lista', kwargs={'publicacion_pk': self.kwargs['publicacion_pk']})
    
class ComentarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Comentario
    template_name = 'comentarios/comentario_eliminar.html'
    """
    Buscar el Comentario basado en comentario_pk
    """
    def get_object(self, queryset=None):
        return get_object_or_404(Comentario, pk=self.kwargs.get('comentario_pk'))
    # Redirigir a la lista de comentarios o a la publicación específica después de borrar un comentario.
    def get_success_url(self):
        return reverse_lazy('comentario_lista', kwargs={'publicacion_pk': self.kwargs['publicacion_pk']})
    
# CATEGORIAS
class CategoriaListView(ListView):
    model = Categoria
    template_name = 'categorias/categoria_lista.html'
    context_object_name = 'categorias'

class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categorias/categoria_crear.html'
    success_url = reverse_lazy('categoria_lista')
    
class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'categorias/categoria_editar.html'
    success_url = reverse_lazy('categoria_lista')
    
class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'categorias/categoria_eliminar.html'
    success_url = reverse_lazy('categoria_lista')
    
# EVENTOS
class EventoListView(ListView):
    model = Evento
    context_object_name = 'eventos'
    template_name = 'eventos/evento_lista.html'
    paginate_by = 5 # 5 eventos por pagina
    
    def get_queryset(self):
        # Ordenar segun fecha de publicacion
        return Evento.objects.all().order_by('-fecha_publicacion')

class EventoDetailView(DetailView):
    model = Evento
    context_object_name = 'evento'
    template_name = 'eventos/evento_detalle.html'

class EventoCreateView(LoginRequiredMixin, CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_crear.html'
    success_url = reverse_lazy('evento_lista')
    
    def form_valid(self, form):
        form.instance.autor = self.request.user  # Usuario logueado como autor
        return super().form_valid(form)

class EventoUpdateView(LoginRequiredMixin, UpdateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_editar.html'
    success_url = reverse_lazy('evento_lista')

class EventoDeleteView(LoginRequiredMixin, DeleteView):
    model = Evento
    template_name = 'eventos/evento_eliminar.html'
    success_url = reverse_lazy('evento_lista')
    
# LOGIN, LOGOUT, REGISTRATION estan en orden 
def login_request(request):
    if request.method =="POST":
        usuario = request.POST['username']
        clave = request.POST['password']
        user = authenticate(request, username=usuario, password=clave)
        if user is not None:
            login(request, user)
            #__Avatar
            try:
                avatar = Avatar.objects.get(user=request.user.id).imagen.url
            except:
                avatar = '/media/avatares/avatar-default.webp'
            finally:
                request.session['avatar'] = avatar
            #____
            
            return redirect(reverse_lazy('index'))
        else:
            return redirect(reverse_lazy('login'))
    else:
        form = AuthenticationForm()
        
    return render(request, 'usuario/login.html', {
        'form': form
    })
    
@login_required
def user_logout(request):
    logout(request)
    return render(request, 'usuario/logout.html')

def register(request):
    if request.method =="POST":
        form = RegistroForm(request.POST)
    
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            form.save()
            return redirect(reverse_lazy('index'))
    else:
        form = RegistroForm()
        
    return render(request, 'usuario/registro.html', {
        'form': form
    })

# EDITAR PERFIL, CAMBIAR CLAVE, AVATAR estan en orden
@login_required
def editProfile(request):
    
    usuario = request.user
    if request.method =="POST":
        form = UserEditForm(request.POST)
    
        if form.is_valid():
            user = User.objects.get(username=usuario)
            
            email = form.cleaned_data.get('email')
            fname = form.cleaned_data.get('first_name')
            lname = form.cleaned_data.get('last_name')
            
            user.email = email
            user.first_name = fname
            user.last_name = lname
            user.save()
            return redirect(reverse_lazy('index'))
    else:
        form = UserEditForm(instance=usuario)
        
    return render(request, 'usuario/editarPerfil.html', {
        'form': form
    })

class CambiarClave(LoginRequiredMixin, PasswordChangeView):
    template_name = 'usuario/cambiar_clave.html'
    success_url = reverse_lazy('index')

@login_required
def agregarAvatar(request):
    if request.method =="POST":
        form = AvatarForm(request.POST, request.FILES)
    
        if form.is_valid():
            usuario = User.objects.get(username=request.user)
            #__ Borrar avatares antiguo del user
            avatarViejo = Avatar.objects.filter(user=usuario)
            if len(avatarViejo) > 0:
                for i in range(len(avatarViejo)):
                    avatarViejo[i].delete()
            #__
            avatar = Avatar(user=usuario, imagen=form.cleaned_data['imagen'])
            
            avatar.save()
            imagen = Avatar.objects.get(user=usuario).imagen.url
            request.session['avatar'] = imagen
            print(f'{imagen}')
            
            return redirect(reverse_lazy('index'))
    else:
        form = AvatarForm()
        
    return render(request, 'usuario/agregarAvatar.html', {
        'form': form
    })