from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.index, name='index'), 
    

    path('eventos/', views.eventos, name='listarEventos'), 
    path('eventos/nuevo/', views.nuevoEvento, name='nuevoEvento'),
    path('eventos/guardar/', views.guardarEvento, name='guardarEvento'),
    path('eventos/editar/<int:id>/', views.editarEvento, name='editarEvento'),
    path('eventos/actualizar/', views.actualizarEvento, name='actualizarEvento'),
    path('eventos/eliminar/<int:id>/', views.eliminarEvento, name='eliminarEvento'),
    
    path('clientes/', views.clientes, name='listarClientes'), 
    path('clientes/nuevo/', views.nuevoCliente, name='nuevoCliente'),
    path('clientes/guardar/', views.guardarCliente, name='guardarCliente'),
    path('clientes/editar/<int:id>/', views.editarCliente, name='editarCliente'),
    path('clientes/eliminar/<int:id>/', views.eliminarCliente, name='eliminarCliente'),
    path('clientes/actualizar/', views.actualizarCliente, name='actualizarCliente'),
    
    path('entradas/', views.listarEntradas, name='listarEntradas'), 
    path('entradas/nueva', views.nuevaEntrada, name='nuevaEntrada'),
    path('entradas/guardar/', views.guardarEntrada, name='guardarEntrada'),
    path('entradas/editar/<uuid:id_unico>/', views.editarEntrada, name='editarEntrada'),
    path('eliminarEntrada/<uuid:id_unico>/', views.eliminarEntrada, name='eliminarEntrada'),
    path('entradas/actualizar/', views.actualizarEntrada, name='actualizarEntrada'),
    path('reporte-ventas/', views.reporte_ventas, name='reporte_ventas'),
]