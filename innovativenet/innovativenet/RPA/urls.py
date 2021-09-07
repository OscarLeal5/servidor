from django.urls import path
from . import views
from .views import (Home, CustomLoginView, Agregar_Cliente, 
    Modificar_Cliente, Eliminar_Cliente, Mostrar_Cliente, 
    Agregar_Servicio,Todos_Clientes, EliminarMantenimiento,
    MttoUpdate, Detalle_Cliente)
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("login/", CustomLoginView.as_view(), name='login'),
    
    path("logout/", LogoutView.as_view(next_page='login'), name='logout'),

    path('', Home.as_view(),name="home"),

    path('clientes',Todos_Clientes.as_view(), name='lista_clientes'),

    path('cotizacion_pdf/<cliente_id>', views.cotizacion_pdf, name='cotizacion_pdf'),

    path('mostrar_cliente/<int:pk>', Mostrar_Cliente.as_view(), name='mostrar_cliente'),

    path('modificar_cliente/<int:pk>/', Modificar_Cliente.as_view(), name='modificar_cliente'),

    path('agregar_cliente', Agregar_Cliente.as_view(), name='agregar_cliente'),

    path('eliminar_cliente/<int:pk>', Eliminar_Cliente.as_view(), name='eliminar_cliente'),

    path('buscar_clientes', views.buscar_clientes, name='buscar_clientes'),

    path('agregar_servicio', Agregar_Servicio.as_view(), name='crear_servicio'),

    path('eliminar_servicio/<int:pk>', EliminarMantenimiento.as_view(), name='eliminar_servicio'),

    path('modificar_servicio/<int:pk>', MttoUpdate.as_view(), name='modificar_servicio'),

    path('detalle_servicio/<int:pk>', Detalle_Cliente.as_view(), name='detalle_servicio'),


]