from django.shortcuts import render, redirect, get_object_or_404
from producto.models import Producto, Categoria, Pedido, DetallePedido
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .forms import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from carro.context_processor import importe_total_carro
from carro.carro import Carro
from django.utils.html import strip_tags
import csv
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.


def home(request):

    productos = Producto.objects.all()
    categorias = Categoria.objects.all()

    queryset = request.GET.get('buscar')

    if queryset:
        productos = Producto.objects.filter(

            Q(nombre__icontains = queryset)
        ).distinct()

    data = {
        'productos': productos,
        'categorias': categorias,

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
    
def admin_pedido(request):

    pedidos = Pedido.objects.all()

    data = {
        'pedidos': pedidos
    }

    return render(request,'administrador/pedidos_admin.html', data)

def export_pedidos_csv(request):
    # Crear la respuesta con el tipo de contenido CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pedidos.csv"'

    # Crear un escritor CSV
    writer = csv.writer(response)
    # Escribir el encabezado del CSV
    writer.writerow(['ID', 'Fecha', 'Total','Cliente'])

    # Obtener todos los registros de pedidos y escribirlos en el CSV
    pedidos = Pedido.objects.all()
    for pedido in pedidos:
        writer.writerow([pedido.pk, pedido.created_at, pedido.total, pedido.user])

    return response


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

def vista_usuario(request):

    total = importe_total_carro(request)
    importe_total = total['importe_total_carro']
    

    status = request.GET.get('status')

    if status == 'approved':
        pedido = Pedido.objects.create(user=request.user,total=importe_total)
            
        carro = Carro(request)

        compra = list()

        for key,value in carro.carro.items():

            compra.append(DetallePedido(

                user = request.user,
                producto_id = key,
                pedido = pedido,
                cantidad = value['cantidad'],
            ))



        DetallePedido.objects.bulk_create(compra)
                            
        enviar_mail(
            pedido=pedido,
            detalle_pedido = compra,
            nombreusuario=request.user.username,
            emailusuario = request.user.email,
            total = importe_total_carro(request)

        )

    else:
        status = 'No existe ninguna pago'
    
    pedido = Pedido.objects.filter(user=request.user)
    detalle = DetallePedido.objects.filter(user=request.user)

    data = {
        'pedidos': pedido,
        'detalle_pedidos': detalle,
        'status':status
    }



    return render(request,'usuario/mis_compras.html', data)

def salir(request):
    logout(request)
    return redirect(to='home:home')

def enviar_mail(**kwargs):

    asunto = 'Gracias por el pedido'

    ctx = {
        'pedido': kwargs.get('pedido'),
        'detalle_pedido': kwargs.get('detalle_pedido'),
        'nombreusuario':kwargs.get('nombreusuario'),
        'total': kwargs.get('total'),
    }

    mensaje =render_to_string('usuario/pedido.html',ctx)

    mensaje_texto = strip_tags(mensaje)
    from_email='nicolas134b@gmail.com'
    to= kwargs.get('emailusuario')

    send_mail(asunto,mensaje_texto,from_email,[to],html_message=mensaje)