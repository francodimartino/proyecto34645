from django.shortcuts import render
from .models import Curso, Profesor
from django.http import HttpResponse

from AppCoder.forms import CursoForm, ProfeForm
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
            return render(request, "AppCoder/inicio.html" ,{"mensaje": "Profesor guardado correctamente"})
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