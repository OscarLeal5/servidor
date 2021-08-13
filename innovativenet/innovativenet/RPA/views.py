from django.shortcuts import render, redirect
from .models import Cliente
from django.http import HttpResponseRedirect
from django.http import  HttpResponse
from .forms import ClienteForm
from django.contrib import messages
#PDF
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch,cm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, Frame,Image
import pandas as pd
from django.db import connection
import dataframe_image as dfi

def modificar_cliente(request,cliente_id):
    cliente = Cliente.objects.get(pk=cliente_id)
    form = ClienteForm(request.POST or None, instance=cliente)
    if form.is_valid():
        form.save()
        return redirect('lista_clientes')

    return render(request,'mantenimientos/modificar_cliente.html',
        {'cliente':cliente,'form':form})

def mostrar_cliente(request, cliente_id):
    cliente = Cliente.objects.get(pk=cliente_id)
    return render(request,'mantenimientos/mostrar_cliente.html',{'cliente':cliente})

def agregar_cliente(request):
    submitted = False
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/agregar_cliente?submitted=True')
    else:
        form = ClienteForm()
        if 'submitted' in request.GET:
            submitted = True
            messages.info(request,'El cliente ha sido agregado exitosamente')
            return redirect('lista_clientes')

    return render(request,'mantenimientos/agregar_cliente.html',{'form':form,'submitted':submitted})


def cotizacion_pdf(request, cliente_id):

    cliente = Cliente.objects.get(pk=cliente_id)

    qs = cliente.dispositivo.values()
    data = pd.DataFrame.from_records(qs)
    dfi.export(data,'datagrame.png')


    nombre=cliente.nombre
    encargado=cliente.encargado
    puesto_encargado=cliente.puesto_encargado
    numero_contacto=cliente.numero_contacto
    correo_contacto=cliente.correo_contacto
    lugar_de_mantenimiento=cliente.lugar_de_mantenimiento
    descripcion_cotizacion=cliente.descripcion_cotizacion
    fecha=cliente.fecha



    #Create bytestream buffer
    buf = io.BytesIO()
    #Create a canvas
    pdf = canvas.Canvas(buf, pagesize=letter,bottomup = 0)

    width, height = letter
    heightList = [
        height * 0.1,
        height * 0.8,
        height * 0.1,
    ]
    mainTable = Table([
        ['header'],
        ['body'],
        ['footer']],
    colWidths=width,
    rowHeights=heightList
    )

    mainTable.wrapOn(pdf,0,0)
    mainTable.drawOn(pdf,0,0)

    #create text object
    textob = pdf.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",14)
    im_data = Image('dataframe.png')
    lines = [
        "linea 1"+nombre,
        "linea 2",
        "linea 3",
    ]
    # mainTable = Table([
    #     ['some text']
    # ])

    for line in lines:
        textob.textLine(line)


    pdf.drawText(textob)
    pdf.drawImage('datagrame.png',10,10)
    pdf.showPage()
    pdf.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True,  filename='cotizacion_'+nombre+'.pdf')


def todos_clientes(request):
    lista_clientes = Cliente.objects.all()
    return render(request,'mantenimientos/Clientes.html',{'lista_clientes':lista_clientes})

def home(request):
    return render(request, 'mantenimientos/home.html',{})
# Create your views here.
