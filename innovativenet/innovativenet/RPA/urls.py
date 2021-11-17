from django.urls import path
from . import views
from .views import * 
from django.contrib.auth.views import LogoutView


urlpatterns = [

    path("login/", CustomLoginView.as_view(), name='login'),
    
    path("logout/", LogoutView.as_view(next_page='login'), name='logout'),

    path('', Home.as_view(),name="home"),

    path('clientes',Todos_Clientes.as_view(), name='lista_clientes'),

    path('cotizacion_pdf/<cliente_id>/<cotizacion_id>/<usuario>', views.cotizacion_pdf, name='cotizacion_pdf'),

    # -------------- CLIENTE -------------------

    path('mostrar_cliente/<int:pk>/', Mostrar_Cliente.as_view(), name='mostrar_cliente'),

    path('modificar_cliente/<int:pk>/', Modificar_Cliente.as_view(), name='modificar_cliente'),

    path('agregar_cliente', Agregar_Cliente.as_view(), name='agregar_cliente'),

    path('eliminar_cliente/<int:pk>', Eliminar_Cliente.as_view(), name='eliminar_cliente'),

    path('buscar_clientes', views.buscar_clientes, name='buscar_clientes'),

    # -------------- SERVICIO -------------------

    path('<int:cliente>/<int:pk>/agregar_servicio/', Agregar_Mantenimiento.as_view(), name='crear_servicio'),

    path('<int:cliente>/<int:pk_cotizacion>/<int:pk>/eliminar_servicio>', EliminarMantenimiento.as_view(), name='eliminar_servicio'),

    path('<int:cliente>/<int:pk_cotizacion>/<int:pk>/modificar_servicio>', MttoUpdate.as_view(), name='modificar_servicio'),

    path('<int:cliente>/<int:pk_cotizacion>/<int:pk>/detalle_servicio', Detalle_Servicio.as_view(), name='detalle_servicio'),

    # -------------- COTIZACION -------------------

    path('<int:cliente>/agregar_cotizacion', Agregar_Cotizacion.as_view(), name='agregar_cotizacion'),

    path('<int:cliente>/<int:pk>/detalle_cotizacion', Detalle_Cotizacion.as_view(), name='detalle_cotizacion'),

    path('<int:cliente>/<int:pk>/eliminar_cotizacion', Eliminar_Cotizacion.as_view(), name='eliminar_cotizacion'),
    
    path('modificar_cotizacion/<int:pk>', Modificar_Cotizacion.as_view(), name='modificar_cotizacion'), 

]
