from django.urls import path
from . import views
from .views import * 
from django.contrib.auth.views import LogoutView


urlpatterns = [

    path("login/", CustomLoginView.as_view(), name='login'),
    
    path("logout/", LogoutView.as_view(next_page='login'), name='logout'),

    path('', Home.as_view(),name="home"),

    path('clientes',Todos_Clientes.as_view(), name='lista_clientes'),


    # -------------- CLIENTE -------------------

    path('mostrar_cliente/<int:pk>/', Mostrar_Cliente.as_view(), name='mostrar_cliente'),

    path('modificar_cliente/<int:pk>/', Modificar_Cliente.as_view(), name='modificar_cliente'),

    path('agregar_cliente', Agregar_Cliente.as_view(), name='agregar_cliente'),

    path('eliminar_cliente/<int:pk>', Eliminar_Cliente.as_view(), name='eliminar_cliente'),

    path('buscar_clientes', views.buscar_clientes, name='buscar_clientes'),

    # -------------- MANTENIMIENTOS DETECCION FUEGO -------------------

    path('<int:cliente>/<int:pk>/agregar_servicio/', Agregar_Mantenimiento.as_view(), name='crear_servicio'),

    path('<int:cliente>/<int:pk_cotizacion>/<int:pk>/eliminar_servicio>', EliminarMantenimiento.as_view(), name='eliminar_servicio'),

    path('<int:cliente>/<int:pk_cotizacion>/<int:pk>/modificar_servicio>', MttoUpdate.as_view(), name='modificar_servicio'),

    path('<int:cliente>/<int:pk_cotizacion>/<int:pk>/detalle_servicio', Detalle_Servicio.as_view(), name='detalle_servicio'),

    # -------------- MANTENIMIENTOS CCTV -------------------

    path('<int:cliente>/<int:pk>/agregar_servicio_cctv/', Agregar_Mantenimiento_CCTV.as_view(), name='crear_servicio_cctv'),

    path('<int:cliente>/<int:pk_cotizacion>/<int:pk>/eliminar_servicio_cctv>', EliminarMantenimiento_CCTV.as_view(), name='eliminar_servicio_cctv'),

    path('<int:cliente>/<int:pk_cotizacion>/<int:pk>/modificar_servicio_cctv>', MttoUpdate_CCTV.as_view(), name='modificar_servicio_cctv'),

    path('<int:cliente>/<int:pk_cotizacion>/<int:pk>/detalle_servicio_cctv', Detalle_Servicio_CCTV.as_view(), name='detalle_servicio_cctv'),

    # -------------- MANTENIMIENTOS CA -------------------

    path('<int:cliente>/<int:pk>/agregar_servicio_ca/', Agregar_Mantenimiento_CA.as_view(), name='crear_servicio_ca'),

    path('<int:cliente>/<int:pk_cotizacion>/<int:pk>/eliminar_servicio_ca>', EliminarMantenimiento_CA.as_view(), name='eliminar_servicio_ca'),

    path('<int:cliente>/<int:pk_cotizacion>/<int:pk>/modificar_servicio_ca>', MttoUpdate_CA.as_view(), name='modificar_servicio_ca'),

    path('<int:cliente>/<int:pk_cotizacion>/<int:pk>/detalle_servicio_ca', Detalle_Servicio_CA.as_view(), name='detalle_servicio_ca'),

    # -------------- COTIZACION -------------------

    path('<int:cliente>/agregar_cotizacion', Agregar_Cotizacion.as_view(), name='agregar_cotizacion'),

    path('<int:cliente>/<int:pk>/detalle_cotizacion', Detalle_Cotizacion.as_view(), name='detalle_cotizacion'),

    path('<int:cliente>/<int:pk>/eliminar_cotizacion', Eliminar_Cotizacion.as_view(), name='eliminar_cotizacion'),
    
    path('modificar_cotizacion/<int:pk>', Modificar_Cotizacion.as_view(), name='modificar_cotizacion'), 
    
    path('cotizacion_pdf/<cliente_id>/<cotizacion_id>/<usuario>', views.cotizacion_pdf, name='cotizacion_pdf'),
    
    path('cotizacion_pdf_us_df/<cliente_id>/<cotizacion_id>/<usuario>', views.contizacion_pdf_us_df, name='cotizacion_pdf_us_df'),
    
    # -------------- COTIZACION CCTV -------------------

    path('<int:cliente>/agregar_cotizacion_cctv', Agregar_Cotizacion_CCTV.as_view(), name='agregar_cotizacion_cctv'),

    path('<int:cliente>/<int:pk>/detalle_cotizacion_cctv', Detalle_Cotizacion_CCTV.as_view(), name='detalle_cotizacion_cctv'),

    path('<int:cliente>/<int:pk>/eliminar_cotizacion_cctv', Eliminar_Cotizacion_CCTV.as_view(), name='eliminar_cotizacion_cctv'),
    
    path('modificar_cotizacion_cctv/<int:pk>', Modificar_Cotizacion_CCTV.as_view(), name='modificar_cotizacion_cctv'), 

    path('cotizacion_pdf_cctv/<cliente_id>/<cotizacion_id>/<usuario>', views.cotizacion_pdf_cctv, name='cotizacion_pdf_cctv'),
    
    path('cotizacion_pdf_us_cctv/<cliente_id>/<cotizacion_id>/<usuario>', views.cotizacion_pdf_us_cctv, name='cotizacion_pdf_us_cctv'),
    
    # -------------- COTIZACION CA -------------------

    path('<int:cliente>/agregar_cotizacion_ca', Agregar_Cotizacion_CA.as_view(), name='agregar_cotizacion_ca'),

    path('<int:cliente>/<int:pk>/detalle_cotizacion_ca', Detalle_Cotizacion_CA.as_view(), name='detalle_cotizacion_ca'),

    path('<int:cliente>/<int:pk>/eliminar_cotizacion_ca', Eliminar_Cotizacion_CA.as_view(), name='eliminar_cotizacion_ca'),
    
    path('modificar_cotizacion_ca/<int:pk>', Modificar_Cotizacion_CA.as_view(), name='modificar_cotizacion_ca'), 

    path('cotizacion_pdf_ca/<cliente_id>/<cotizacion_id>/<usuario>', views.cotizacion_pdf_ca, name='cotizacion_pdf_ca'),
    
    path('cotizacion_pdf_us_ca/<cliente_id>/<cotizacion_id>/<usuario>', views.cotizacion_pdf_us_ca, name='cotizacion_pdf_us_ca'),

]
 