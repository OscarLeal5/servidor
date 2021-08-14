from django.shortcuts import render, redirect
from .models import Cliente
from django.http import HttpResponseRedirect
from django.http import  HttpResponse
from .forms import ClienteForm
from django.contrib import messages
#PDF
from django.http import FileResponse
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors

from datetime import datetime

def eliminar_cliente(request,cliente_id):
    cliente = Cliente.objects.get(pk=cliente_id)
    cliente.delete()
    messages.error(request, 'El cliente ha sido eliminado exitosamente')
    return redirect('lista_clientes')

def modificar_cliente(request,cliente_id):
    cliente = Cliente.objects.get(pk=cliente_id)
    form = ClienteForm(request.POST or None, instance=cliente)
    if form.is_valid():
        form.save()
        messages.info(request, 'El cliente ha sido modificado exitosamente')
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
            messages.success(request, 'El cliente ha sido agregado exitosamente')
            return redirect('lista_clientes')

    return render(request,'mantenimientos/agregar_cliente.html',{'form':form,'submitted':submitted})


def cotizacion_pdf(request, cliente_id):

    cliente = Cliente.objects.get(pk=cliente_id)
    buf = io.BytesIO()

    nombre=cliente.nombre
    encargado=cliente.encargado
    puesto_encargado=cliente.puesto_encargado
    numero_contacto=cliente.numero_contacto
    correo_contacto=cliente.correo_contacto
    lugar_de_mantenimiento=cliente.lugar_de_mantenimiento
    descripcion_cotizacion=cliente.descripcion_cotizacion
    fecha=cliente.fecha



    dateTimeObj = datetime.now()
    dateObj = dateTimeObj.date()
    dateStr = dateObj.strftime("%b %d , %Y")

    PAGE_HEIGHT = defaultPageSize[1];
    PAGE_WIDTH = defaultPageSize[0]
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Normal_R',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_RIGHT,
                              fontSize=12,
                              textColor=colors.black,
                              ))
    Title = "Hello world"

    def myFirstPage(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Bold', 16)
        canvas.setFont('Times-Roman', 14)
        header = []
        canvas.drawImage('RPA/logo.png', 0.8 * inch, 660, width=160, height=80)
        canvas.drawImage('RPA/lenellogo.png', 6.5 * inch, 660, width=80, height=80)
        canvas.drawImage('RPA/footer.png', inch, 1, width=460, height=80)
        canvas.restoreState()

    def myLaterPages(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.drawImage('logo.png', 0.8 * inch, 660, width=160, height=80)
        canvas.drawImage('lenellogo.png', 6.5 * inch, 660, width=80, height=80)
        canvas.drawImage('footer.png', inch, 1, width=460, height=80)
        canvas.restoreState()

    def go():
        cliente = Cliente.objects.get(pk=cliente_id)
        doc = SimpleDocTemplate(buf, pagesize=letter,
                                rightMargin=inch, leftMargin=inch,
                                topMargin=2 * inch, bottomMargin=inch)
        encargado = cliente.encargado
        puesto = cliente.puesto_encargado
        cliente = cliente.nombre

        Story = []

        styleN = styles["Normal"]
        styleH4 = styles["Heading4"]
        styleH2 = styles["Heading2"]

        styleRight = styles["Normal_R"]

        texto_fecha = ("Tijuana, B.C. a " + dateStr)
        texto_encargado = ("Attn. " + encargado)

        p0 = Paragraph(texto_fecha, styleRight)
        p1 = Paragraph(texto_encargado, styleH4)
        p2 = Paragraph(puesto, styleN)
        p3 = Paragraph(cliente, styleH2)

        Story.append(p0)
        Story.append(p1)
        Story.append(p2)
        Story.append(p3)

        doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
        # doc.build(Story)
    go()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True,  filename='cotizacion_'+nombre+'.pdf')


def todos_clientes(request):
    lista_clientes = Cliente.objects.all()
    return render(request,'mantenimientos/Clientes.html',{'lista_clientes':lista_clientes})

def home(request):
    return render(request, 'mantenimientos/home.html',{})
# Create your views here.
