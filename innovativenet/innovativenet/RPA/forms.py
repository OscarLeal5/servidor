from django import forms
from django.forms import ModelForm
from .models import Cliente

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"
        #('nombre','encargado','puesto_encargado','numero_contacto','correo_contacto','lugar_de_mantenimiento','descripcion_cotizacion','fecha','mantenimiento','dispositivo')
        labels = {
            'nombre':'',
            'encargado': '',
            'puesto_encargado': '',
            'numero_contacto': '',
            'correo_contacto': '',
            'lugar_de_mantenimiento': '',
            'descripcion_cotizacion': '',
            'fecha': '',
            'mantenimiento': 'Servicios de mantenimiento requeridos',
            'dispositivo': 'Dispositivos a los que se realizara mantenimiento',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre de la compañia'}),
            'encargado': forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre del encargado dentro de la compañia'}),
            'puesto_encargado': forms.TextInput(attrs={'class':'form-control','placeholder':'Puesto del encargado'}),
            'numero_contacto': forms.TextInput(attrs={'class':'form-control','placeholder':'Numero de contacto'}),
            'correo_contacto': forms.EmailInput(attrs={'class':'form-control','placeholder':'Correo de contacto'}),
            'lugar_de_mantenimiento': forms.TextInput(attrs={'class':'form-control','placeholder':'Lugar donde se realizara el mantenimiento'}),
            'descripcion_cotizacion': forms.Textarea(attrs={'class':'form-control','placeholder':'Descripcion del mantenimiento a realizarse'}),
            'fecha': forms.DateInput(attrs={'class':'form-control','placeholder':'Fecha programada para el mantenimiento'}),
            'mantenimiento': forms.SelectMultiple(attrs={'class':'form-control','placeholder':'Servicios de mantenimiento necesarios'}),
            'dispositivo': forms.SelectMultiple(attrs={'class':'form-control','placeholder':'Dispositivos a los que se realizara mantenimiento'}),

        }