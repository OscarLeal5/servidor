from django.urls import path
from . import views
from .views import Home, CustomLoginView, Agregar_Cliente, Modificar_Cliente, Eliminar_Cliente, Mostrar_Cliente, Agregar_Servicio
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("login/", CustomLoginView.as_view(), name='login'),
    
    path("logout/", LogoutView.as_view(next_page='login'), name='logout'),

    path('', Home.as_view(),name="home"),

    path('clientes',views.todos_clientes, name='lista_clientes'),

    path('cotizacion_pdf/<cliente_id>', views.cotizacion_pdf, name='cotizacion_pdf'),

    path('mostrar_cliente/<int:pk>', Mostrar_Cliente.as_view(), name='mostrar_cliente'),
    # path('mostrar_cliente/<cliente_id>', views.mostrar_cliente, name='mostrar_cliente'),

    path('modificar_cliente/<int:pk>/', Modificar_Cliente.as_view(), name='modificar_cliente'),
    # path('modificar_cliente/<cliente_id>', views.modificar_cliente, name='modificar_cliente'),

    path('agregar_cliente', Agregar_Cliente.as_view(), name='agregar_cliente'),
    # path('agregar_cliente', views.agregar_cliente, name='agregar_cliente'),

    path('eliminar_cliente/<int:pk>', Eliminar_Cliente.as_view(), name='eliminar_cliente'),
    # path('eliminar_cliente/<cliente_id>', views.eliminar_cliente, name='eliminar_cliente'),

    path('buscar_clientes', views.buscar_clientes, name='buscar_clientes'),

    path('agregar_servicio', Agregar_Servicio.as_view(), name='crear_servicio')


]