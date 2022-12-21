from django.shortcuts import render
from .models import Curso, Profesor, Estudiante
from django.http import HttpResponse

from django.urls import reverse_lazy

from AppCoder.forms import CursoForm, ProfeForm, RegistroUsuarioForm

from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate


from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.decorators import login_required #para vistas basadas en funciones DEF  
from django.contrib.auth.mixins import LoginRequiredMixin #para vistas basadas en clases CLASS   

# Create your views here.
@login_required
def curso(request):

    cursito= Curso(nombre="JavaScript", comision=123456)
    cursito.save()
    cadena_texto=f"curso guardado: Nombre: {cursito.nombre}, Comision: {cursito.comision}"
    return HttpResponse(cadena_texto)

@login_required
def cursos(request):
    return render (request, "AppCoder/cursos.html")
@login_required
def estudiantes(request):
    return render (request, "AppCoder/estudiantes.html")
@login_required
def profesores(request):
    return render (request, "AppCoder/profesores.html")
@login_required
def entregables(request):
    return render (request, "AppCoder/entregables.html")

def inicio(request):
    return render (request, "AppCoder/inicio.html")

""" def cursoFormulario(request):
    if request.method=="POST":
        nombre= request.POST["nombre"]
        comision= request.POST["comision"]
        print(nombre, comision)
        curso= Curso(nombre=nombre, comision=comision)
        curso.save()
        return render(request, "AppCoder/inicio.html" ,{"mensaje": "Curso guardado correctamente"})
        
    else:
        return render (request, "AppCoder/cursoFormulario.html") """

@login_required
def cursoFormulario(request):
    if request.method=="POST":
        form= CursoForm(request.POST)
        print("-------------------------------")
        print(form)
        print("-------------------------------")
        if form.is_valid():
            informacion=form.cleaned_data #convierte de la info en modo formulario a un diccionario
            print(informacion)
            nombre= informacion["nombre"]
            comision= informacion["comision"]
            curso= Curso(nombre=nombre, comision=comision)
            curso.save()
            return render(request, "AppCoder/inicio.html" ,{"mensaje": "Curso guardado correctamente"})
        else:
            return render(request, "AppCoder/cursoFormulario.html" ,{"form": form, "mensaje": "Informacion no valida"})
        
    else:
        formulario= CursoForm()
        return render (request, "AppCoder/cursoFormulario.html", {"form": formulario})
@login_required
def profeFormulario(request):
    if request.method=="POST":
        form= ProfeForm(request.POST)
        
        if form.is_valid():
            informacion=form.cleaned_data
            nombre= informacion["nombre"]
            apellido= informacion["apellido"]
            email= informacion["email"]
            profesion= informacion["profesion"]
            profe= Profesor(nombre=nombre, apellido=apellido, email=email, profesion=profesion)
            profe.save()
            profesores=Profesor.objects.all()
            return render(request, "AppCoder/Profesores.html" ,{"profesores":profesores, "mensaje": "Profesor guardado correctamente"})
        else:
            return render(request, "AppCoder/ProfeFormulario.html" ,{"form": form, "mensaje": "Informacion no valida"})
        
    else:
        formulario= ProfeForm()
        return render (request, "AppCoder/ProfeFormulario.html", {"form": formulario})
@login_required
def busquedaComision(request):
    return render(request, "AppCoder/busquedaComision.html")
@login_required
def buscar(request):
    
    comision= request.GET["comision"]
    if comision!="":
        cursos= Curso.objects.filter(comision__icontains=comision)#buscar otros filtros en la documentacion de django
        return render(request, "AppCoder/resultadosBusqueda.html", {"cursos": cursos})
    else:
        return render(request, "AppCoder/busquedaComision.html", {"mensaje": "Che Ingresa una comision para buscar!"})


    
@login_required
def leerProfesores(request):

    profesores=Profesor.objects.all()
    return render(request, "AppCoder/Profesores.html", {"profesores": profesores})

@login_required
def eliminarProfesor(request, id):
    profesor=Profesor.objects.get(id=id)
    print(profesor)
    profesor.delete()
    profesores=Profesor.objects.all()
    return render(request, "AppCoder/Profesores.html", {"profesores": profesores, "mensaje": "Profesor eliminado correctamente"})

@login_required
def editarProfesor(request, id):
    profesor=Profesor.objects.get(id=id)
    if request.method=="POST":
        form= ProfeForm(request.POST)
        if form.is_valid():
            info=form.cleaned_data
            profesor.nombre=info["nombre"]
            profesor.apellido=info["apellido"]
            profesor.email=info["email"]
            profesor.profesion=info["profesion"]
            profesor.save()
            profesores=Profesor.objects.all()
            return render(request, "AppCoder/Profesores.html" ,{"profesores":profesores, "mensaje": "Profesor editado correctamente"})
        pass
    else:
        formulario= ProfeForm(initial={"nombre":profesor.nombre, "apellido":profesor.apellido, "email":profesor.email, "profesion":profesor.profesion})
        return render(request, "AppCoder/editarProfesor.html", {"form": formulario, "profesor": profesor})



#....... VISTAS BASADAS EN CLASES

class EstudianteList(LoginRequiredMixin, ListView):#vista usada para LISTAR
    model= Estudiante
    template_name= "AppCoder/estudiantes.html"

class EstudianteCreacion(LoginRequiredMixin,CreateView):#vista usada para CREAR
    model= Estudiante
    success_url= reverse_lazy("estudiante_list")
    fields=['nombre', 'apellido', 'email']

class EstudianteUpdate(LoginRequiredMixin,UpdateView):#vista usada para EDITAR
    model = Estudiante
    success_url = reverse_lazy('estudiante_list')
    fields=['nombre', 'apellido', 'email']
    
class EstudianteDetalle(LoginRequiredMixin,DetailView): #vista usada para MOSTRAR DATOS
    model=Estudiante
    template_name="Appcoder/estudiante_detalle.html"

class EstudianteDelete(LoginRequiredMixin,DeleteView):#vista usada para ELIMINAR
    model = Estudiante
    success_url = reverse_lazy('estudiante_list')



# vista de registro

def register(request):
    if request.method=="POST":
        form= RegistroUsuarioForm(request.POST)
        if form.is_valid():
            username= form.cleaned_data.get("username")
            form.save()
            return render(request, "AppCoder/inicio.html", {"mensaje":f"Usuario {username} creado correctamente"})
        else:
            return render(request, "AppCoder/register.html", {"form": form, "mensaje":"Error al crear el usuario"})
    else:
        form= RegistroUsuarioForm()
        return render(request, "AppCoder/register.html", {"form": form})

def login_request(request):
    if request.method=="POST":
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            info=form.cleaned_data
            usu=info["username"]
            clave=info["password"]
            usuario=authenticate(username=usu, password=clave)#verifica si el usuario existe, si existe, lo devuelve, y si no devuelve None 
            if usuario is not None:
                login(request, usuario)
                return render(request, "AppCoder/inicio.html", {"mensaje":f"Usuario {usu} logueado correctamente"})
            else:
                return render(request, "AppCoder/login.html", {"form": form, "mensaje":"Usuario o contraseña incorrectos"})
        else:
            return render(request, "AppCoder/login.html", {"form": form, "mensaje":"Usuario o contraseña incorrectos"})
    else:
        form=AuthenticationForm()
        return render(request, "AppCoder/login.html", {"form": form})