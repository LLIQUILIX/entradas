from django.shortcuts import render, redirect, get_object_or_404
from .models import Evento, Cliente, Entrada
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.utils import timezone
from django.db.models import Sum, F
from django.db.models.functions import Round

# =====================================
#cursos
# ==========================================


@login_required
def index(request):
    eventos = Evento.objects.all()
    
    total_eventos = Evento.objects.count()
    total_clientes = Cliente.objects.count()
    total_entradas = Entrada.objects.count()
    eventos = Evento.objects.all()
    # Calculamos cupos para cada evento
    for e in eventos:
        vendidas = Entrada.objects.filter(evento=e).count()
        e.disponibles = e.capacidad_total - vendidas
    
    return render(request, 'index.html', {
        'total_eventos': total_eventos,
        'total_clientes': total_clientes,
        'total_entradas': total_entradas,
        'eventos': eventos
        
    })
# =====================================
# EVENTOS
# =====================================

@login_required
def eventos(request):
    
    eventos = Evento.objects.annotate(vendidas=Count('entrada'))
    return render(request, "Eventos.html", {'eventos': eventos})


def nuevoEvento(request):
    
    eventos = Evento.objects.all()
    return render(request, "nuevo_evento.html", {'evento': eventos})

def guardarEvento(request):
    if request.method == 'POST':
        # Captura de datos del formulario
        nombre = request.POST.get('nombre')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora_inicio')
        capacidad = request.POST.get('capacidad_total')
        precio = request.POST.get('precio')
        foto = request.FILES.get('foto')

        # Persistencia en la base de datos
        Evento.objects.create(
            nombre=nombre,
            fecha=fecha,
            hora_inicio=hora,
            capacidad_total=capacidad,
            precio=precio,
            foto=foto
        )
        messages.success(request, 'Evento guardado exitosamente')
        return redirect('listarEventos')

@login_required    
def editarEvento(request, id):

    evento = get_object_or_404(Evento, id=id)
    
    return render(request, "editar_evento.html", {
        'evento': evento  
    })


@login_required
def actualizarEvento(request):
    # Verificamos que la petición sea POST para seguridad
    if request.method == 'POST':
        # Captura segura del ID
        id_evento = request.POST.get('id')
        evento = get_object_or_404(Evento, id=id_evento)
        nombre = request.POST.get('nombre')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora_inicio')
        capacidad = request.POST.get('capacidad_total')
        precio = request.POST.get('precio')

    
        entradas_vendidas = evento.entrada_set.count() 
        if int(capacidad) < entradas_vendidas:
            messages.error(request, f'Error: No puedes reducir la capacidad a {capacidad} porque ya has vendido {entradas_vendidas} entradas.')
            return redirect('editarEvento', id=id_evento)

        # Actualización del objeto
        evento.nombre = nombre
        evento.fecha = fecha
        evento.hora_inicio =hora
        evento.capacidad_total = capacidad
        evento.precio = precio
    
        if request.FILES.get('foto'):
            evento.foto = request.FILES.get('foto')

        evento.save()
        messages.success(request, 'Evento actualizado exitosamente.')
        return redirect('listarEventos')
    
    return redirect('listarEventos')


@login_required
def eliminarEvento(request, id):
    try:
        evento = Evento.objects.get(id=id)
        # Validación: No eliminar si ya hay entradas vendidas (Regla de negocio)
        if evento.entrada_set.exists():
            messages.error(request, 'No se puede eliminar: Ya existen entradas vendidas.')
        else:
            evento.delete()
            messages.success(request, 'Evento eliminado.')
    except Exception as e:
        messages.error(request, 'Error al eliminar.')
    return redirect('listarEventos')



# =====================================
# CLIENTES
# =====================================

@login_required
def clientes(request):
    
    clientes = Cliente.objects.all()
    return render(request, "clientes.html", {'clientes': clientes})


@login_required
def nuevoCliente(request):
    
    clientes = Cliente.objects.all()
    return render(request, "nuevo_cliente.html", {'clientes': clientes})

@login_required
def guardarCliente(request):
    if request.method == 'POST':
        
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')

    
        if Cliente.objects.filter(email=email).exists():
            messages.error(request, f'El correo {email} ya está registrado con otro cliente.')
            return redirect('nuevoCliente')

   
        try:
            Cliente.objects.create(
                nombre=nombre,
                email=email,
                telefono=telefono
            )
            messages.success(request, 'Cliente registrado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al guardar: {e}')
            return redirect('nuevoCliente')
            
        return redirect('listarClientes')

@login_required
def eliminarCliente(request, id):
  
    cliente = get_object_or_404(Cliente, id=id)
    try:
        if cliente.entrada_set.exists():
            messages.error(request, 'No se puede eliminar: El cliente tiene entradas Registradas.')
        else:
            cliente.delete()
            messages.success(request, 'Cliente eliminado correctamente.')
    except Exception as e:
        messages.error(request, 'Ocurrió un error inesperado al intentar eliminar.')
        
    return redirect('listarClientes')

@login_required
def editarCliente(request, id):

    cliente = get_object_or_404(Cliente, id=id)
    return render(request, "editar_cliente.html", {
        'clientes': cliente
    })

@login_required
def actualizarCliente(request):
    if request.method == 'POST':

        id_cliente = request.POST.get('id')
        cliente = get_object_or_404(Cliente, id=id_cliente)
        
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        if Cliente.objects.filter(email=email).exclude(id=id_cliente).exists():
            messages.error(request, f'Error: El correo {email} ya pertenece a otro cliente.')
            return redirect('editarCliente', id=id_cliente)

        cliente.nombre = nombre
        cliente.email = email
        cliente.telefono = telefono
        cliente.save()

        messages.success(request, 'Cliente actualizado con éxito.')
        return redirect('listarClientes')


# =====================================
# CLIENTES
# =====================================

@login_required
def listarEntradas(request):
    entradas = Entrada.objects.all().select_related('evento', 'cliente')
    return render(request, "entradas.html", {'entradas': entradas})

# Formulario para nueva venta

@login_required
def nuevaEntrada(request):
    eventos = Evento.objects.all()
    clientes = Cliente.objects.all()
    return render(request, "nueva_entrada.html", {
        'eventos': eventos,
        'clientes': clientes
    })


@login_required
def guardarEntrada(request):
    if request.method == 'POST':
        id_evento = request.POST.get('evento')
        id_cliente = request.POST.get('cliente')
        
        evento = get_object_or_404(Evento, id=id_evento)
        cliente = get_object_or_404(Cliente, id=id_cliente)

        if evento.entradas_disponibles <= 0:
            messages.error(request, f"¡Agotado! No hay más cupos.")
            return redirect('nuevaEntrada')

        nueva_entrada = Entrada.objects.create(evento=evento, cliente=cliente)

        try:
        
            fecha_txt = evento.fecha.strftime("%d/%m/%Y")
            hora_txt = evento.hora_inicio.strftime("%H:%M") # Formato 24h
            
            asunto = f"Confirmación: {evento.nombre} - UTC"
            
            html_mensaje = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 20px;">
                        <h2 style="color: #157347; text-align: center;">¡Entrada Confirmada!</h2>
                        <p>Hola <strong>{cliente.nombre}</strong>,</p>
                        <p>Se ha registrado tu entrada exitosamente para el siguiente evento:</p>
                        <hr>
                        <p><strong>Evento:</strong> {evento.nombre}</p>
                        <p><strong>Fecha:</strong> {fecha_txt}</p>
                        <p><strong>Hora de Inicio:</strong> {hora_txt}</p>
                        <p><strong>Código de Acceso :</strong></p>
                        <div style="background: #f4f4f4; padding: 10px; border: 1px dashed #999; text-align: center;">
                            <code style="font-size: 1.1em;">{nueva_entrada.id_unico}</code>
                        </div>
                        <hr>
                        <p style="font-size: 0.9em; color: #666;">Presenta este código al momento de ingresar.</p>
                    </div>
                </body>
            </html>
            """
            
            email = EmailMessage(
                asunto,
                html_mensaje,
                settings.EMAIL_HOST_USER,
                [cliente.email]
            )
            email.content_subtype = "html"
            email.send()

            messages.success(request, f"Venta exitosa. Código enviado a {cliente.email}")
            
        except Exception as e:
            messages.warning(request, f"Entrada guardada, pero el correo falló: {e}")

        return redirect('listarEntradas')

@login_required   
def editarEntrada(request, id_unico):
    
    entrada = get_object_or_404(Entrada, id_unico=id_unico)
    eventos = Evento.objects.all()
    clientes = Cliente.objects.all()
    
    return render(request, "editar_entrada.html", {
        'entrada': entrada,
        'eventos': eventos,
        'clientes': clientes
    })

@login_required
def actualizarEntrada(request):
    if request.method == 'POST':
        
        id_entrada = request.POST.get('id_unico')
        entrada = get_object_or_404(Entrada, id_unico=id_entrada)
        
     
        id_evento_nuevo = request.POST.get('evento')
        id_cliente = request.POST.get('cliente')
        
        evento_nuevo = get_object_or_404(Evento, id=id_evento_nuevo)
        cliente = get_object_or_404(Cliente, id=id_cliente)

        if entrada.evento.id != int(id_evento_nuevo):
            if evento_nuevo.entradas_disponibles <= 0:
                messages.error(request, f"¡Error! El evento '{evento_nuevo.nombre}' no tiene cupos disponibles.")
                return redirect('editarEntrada', id_unico=id_entrada)

    
        entrada.evento = evento_nuevo
        entrada.cliente = cliente
        entrada.save()

        messages.success(request, 'Entrada actualizada correctamente.')
        return redirect('listarEntradas')
    
    return redirect('listarEntradas')

@login_required
def eliminarEntrada(request, id_unico):

    entrada = get_object_or_404(Entrada, id_unico=id_unico)
    
    try:

        nombre_evento = entrada.evento.nombre
        cliente_nombre = entrada.cliente.nombre
        
        entrada.delete()
        
        messages.success(request, f'La entrada de {cliente_nombre} para {nombre_evento} ha sido anulada.')
    except Exception as e:
        messages.error(request, f'Ocurrió un error al intentar eliminar la entrada: {e}')
        
    return redirect('listarEntradas')


@login_required
def reporte_ventas(request):
  
    eventos_reporte = Evento.objects.annotate(
        entradas_vendidas=Count('entrada'),
       
        total_recaudado=Round(Sum(F('entrada__evento__precio')), 2)
    )
    return render(request, 'reporte.html', {'reporte': eventos_reporte})