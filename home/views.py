from django.shortcuts import render, redirect, get_object_or_404
from producto.models import Producto, Categoria
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .forms import CustomUser
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def home(request):

    productos = Producto.objects.all()
    categorias = Categoria.objects.all()

    data = {
        'productos': productos,
        'categorias': categorias
    }

    return render(request, 'index.html', data)


def admin(request):

    if request.user.is_staff:
    
        productos = Producto.objects.all()
        categorias = Categoria.objects.all()

        data = {
            'productos': productos,
            'categorias': categorias
        }

        if request.method != 'POST':
            return render(request, 'administrador/admin.html', data)
        else:
            imagen = request.FILES.get('imagen')
            nombre = request.POST['nombre']
            descipcion = request.POST['desc']
            seccion = request.POST['seccion']
            precio = request.POST['precio']

            categoria = Categoria.objects.get(nombre=seccion)

            objProducto = Producto.objects.create(
                imagen=imagen,
                nombre=nombre,
                descripcion=descipcion,
                precio=precio,
                categoria=categoria,
                # stock = stock,
            )
            objProducto.save()

            # messages.success(request,'Producto creado correctamente')

            # return redirect(to='admin_page:productos')

            return render(request, 'administrador/admin.html', data)
        
    else:
        return redirect(to='home:home')


def eliminar(request, id):

    producto = get_object_or_404(Producto, id=id)
    producto.delete()

    return redirect(to='home:administrador')


# seccion de contacto
def contacto(request):

    if request.method =='POST':

        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        template = render_to_string('Contacto/email_cointacto.html', {
            'name':name,
            'email':email,
            'message':message
        })

        email = EmailMessage(
            subject,
            template,
            settings.EMAIL_HOST_USER,
            ['nicolas134b@gmail.com']
        )

        email.content_subtype = 'html'

        email.fail_silently = False
        email.send()

        messages.success(request,'Se ha enviado el correo')

        return redirect(to='home:contacto')

        


    return render(request, 'contacto/Contacto.html', )

def registro(request):

    data = {
        'form':CustomUser()
    }

    if request.method == 'POST':
        formulario = CustomUser(data = request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username = formulario.cleaned_data["username"], password = formulario.cleaned_data["password1"])
            messages.success(request, 'Registrado correctamente')
            login(request, user)
            return redirect(to='home:home')
        data["form"] = formulario

    return render(request,'registration/registro.html',data)

def salir(request):
    logout(request)
    return redirect(to='home:home')