from django.urls import path
from . import views
from .views import Mantenimientos, CustomLoginView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("login/", CustomLoginView.as_view(), name='login'),
    
    path("logout/", LogoutView.as_view(next_page='login'), name='logout'),

    path('', Mantenimientos.as_view(),name="home"),

    path('clientes',views.todos_clientes, name='lista_clientes'),

    path('cotizacion_pdf/<cliente_id>', views.cotizacion_pdf, name='cotizacion_pdf'),

    path('mostrar_cliente/<cliente_id>', views.mostrar_cliente, name='mostrar_cliente'),

    path('modificar_cliente/<cliente_id>', views.modificar_cliente, name='modificar_cliente'),

    path('agregar_cliente', views.agregar_cliente, name='agregar_cliente'),

    path('eliminar_cliente/<cliente_id>', views.eliminar_cliente, name='eliminar_cliente'),


]