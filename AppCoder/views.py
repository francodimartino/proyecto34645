from django.shortcuts import render
from .models import Curso, Profesor, Estudiante
from django.http import HttpResponse

from django.urls import reverse_lazy

from AppCoder.forms import CursoForm, ProfeForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Create your views here.

def curso(request):

    cursito= Curso(nombre="JavaScript", comision=123456)
    cursito.save()
    cadena_texto=f"curso guardado: Nombre: {cursito.nombre}, Comision: {cursito.comision}"
    return HttpResponse(cadena_texto)


def cursos(request):
    return render (request, "AppCoder/cursos.html")

def estudiantes(request):
    return render (request, "AppCoder/estudiantes.html")

def profesores(request):
    return render (request, "AppCoder/profesores.html")

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

def busquedaComision(request):
    return render(request, "AppCoder/busquedaComision.html")

def buscar(request):
    
    comision= request.GET["comision"]
    if comision!="":
        cursos= Curso.objects.filter(comision__icontains=comision)#buscar otros filtros en la documentacion de django
        return render(request, "AppCoder/resultadosBusqueda.html", {"cursos": cursos})
    else:
        return render(request, "AppCoder/busquedaComision.html", {"mensaje": "Che Ingresa una comision para buscar!"})


    

def leerProfesores(request):

    profesores=Profesor.objects.all()
    return render(request, "AppCoder/Profesores.html", {"profesores": profesores})


def eliminarProfesor(request, id):
    profesor=Profesor.objects.get(id=id)
    print(profesor)
    profesor.delete()
    profesores=Profesor.objects.all()
    return render(request, "AppCoder/Profesores.html", {"profesores": profesores, "mensaje": "Profesor eliminado correctamente"})


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

class EstudianteList(ListView):#vista usada para LISTAR
    model= Estudiante
    template_name= "AppCoder/estudiantes.html"

class EstudianteCreacion(CreateView):#vista usada para CREAR
    model= Estudiante
    success_url= reverse_lazy("estudiante_list")
    fields=['nombre', 'apellido', 'email']

class EstudianteUpdate(UpdateView):#vista usada para EDITAR
    model = Estudiante
    success_url = reverse_lazy('estudiante_list')
    fields=['nombre', 'apellido', 'email']
    
class EstudianteDetalle(DetailView): #vista usada para MOSTRAR DATOS
    model=Estudiante
    template_name="Appcoder/estudiante_detalle.html"

class EstudianteDelete(DeleteView):#vista usada para ELIMINAR
    model = Estudiante
    success_url = reverse_lazy('estudiante_list')
