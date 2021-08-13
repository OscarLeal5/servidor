from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('clientes',views.todos_clientes, name='lista_clientes'),
    path('cotizacion_pdf/<cliente_id>', views.cotizacion_pdf, name='cotizacion_pdf'),
    path('mostrar_cliente/<cliente_id>', views.mostrar_cliente, name='mostrar_cliente'),
    path('modificar_cliente/<cliente_id>', views.modificar_cliente, name='modificar_cliente'),
    path('agregar_cliente', views.agregar_cliente, name='agregar_cliente'),
    path('eliminar_cliente/<cliente_id>', views.eliminar_cliente, name='eliminar_cliente'),

]