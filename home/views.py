from django.shortcuts import render, redirect, get_object_or_404
from producto.models import Producto, Categoria
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
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
