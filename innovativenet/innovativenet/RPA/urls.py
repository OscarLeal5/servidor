from django.urls import path
from . import views
from .views import * 
from django.contrib.auth.views import LogoutView


urlpatterns = [

    path("login/", CustomLoginView.as_view(), name='login'),
    
    path("logout/", LogoutView.as_view(next_page='login'), name='logout'),

    path('', Home.as_view(),name="home"),

    path('clientes',Todos_Clientes.as_view(), name='lista_clientes'),

    path('cotizacion_pdf/<cliente_id>', views.cotizacion_pdf, name='cotizacion_pdf'),

    # -------------- CLIENTE -------------------

    path('mostrar_cliente/<int:pk>/', Mostrar_Cliente.as_view(), name='mostrar_cliente'),

    path('modificar_cliente/<int:pk>/', Modificar_Cliente.as_view(), name='modificar_cliente'),

    path('agregar_cliente', Agregar_Cliente.as_view(), name='agregar_cliente'),

    path('eliminar_cliente/<int:pk>', Eliminar_Cliente.as_view(), name='eliminar_cliente'),
    path('buscar_clientes', views.buscar_clientes, name='buscar_clientes'),

    # -------------- SERVICIO -------------------

    path('<int:cliente>/<int:pk>/agregar_servicio/', Agregar_Mantenimiento.as_view(), name='crear_servicio'),

    path('<int:cotizacion>/eliminar_servicio>', EliminarMantenimiento.as_view(), name='eliminar_servicio'),

    path('<int:cotizacion>/modificar_servicio>', MttoUpdate.as_view(), name='modificar_servicio'),

    path('<int:cliente>/<int:pk>/detalle_servicio', Detalle_Servicio.as_view(), name='detalle_servicio'),

    # -------------- DISPOSITIVO -------------------

    path('agregar_dispositivo/<int:pk>', Agregar_Dispositivo.as_view(), name='crear_dispositivo'),

    path('eliminar_dispositivo/<int:pk>', Eliminar_Dispositivo.as_view(), name='eliminar_dispositivo'),

    path('modificar_dispositivo/<int:pk>', Update_Dispositivo.as_view(), name='modificar_dispositivo'),

    path('detalle_dispositivo/<int:pk>', Detalle_Dispositivo.as_view(), name='detalle_dispositivo'),

    # -------------- COTIZACION -------------------

    path('<int:cliente>/agregar_cotizacion', Agregar_Cotizacion.as_view(), name='agregar_cotizacion'),

    path('<int:cliente>/<int:pk>/detalle_cotizacion', Detalle_Cotizacion.as_view(), name='detalle_cotizacion'),

    path('eliminar_cotizacion/<int:pk>', Eliminar_Cotizacion.as_view(), name='eliminar_cotizacion'),
    
    path('modificar_cotizacion/<int:pk>', Modificar_Cotizacion.as_view(), name='modificar_cotizacion'), 

]
