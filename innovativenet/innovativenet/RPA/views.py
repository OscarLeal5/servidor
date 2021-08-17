from django.shortcuts import render, redirect
from reportlab.pdfgen import canvas

from .models import Cliente
from django.http import HttpResponseRedirect
from django.http import  HttpResponse
from .forms import ClienteForm
from django.contrib import messages
#PDF
from django.http import FileResponse
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table,TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors

from datetime import datetime
from datetime import date

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

    actyear = str(date.today().year)
    sigyear = str(date.today().year + 1)

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
    styles.add(ParagraphStyle(name='Normal_C',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.black,
                              ))

    styles.add(ParagraphStyle(name='Heading1_B',
                              parent=styles['Heading1'],
                              wordWrap='LTR',
                              alignment=TA_LEFT,
                              fontSize=12,
                              textColor=colors.HexColor("#3498DB"),
                              ))
    styles.add(ParagraphStyle(name='Heading1_BC',
                              parent=styles['Heading1'],
                              wordWrap='LTR',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.HexColor("#3498DB"),
                              ))

    styles.add(ParagraphStyle(name='Normal_CB',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              ))
    styles.add(ParagraphStyle(name='Normal_B',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_LEFT,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              ))

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
        canvas.drawImage('RPA/logo.png', 0.8 * inch, 660, width=160, height=80)
        canvas.drawImage('RPA/lenellogo.png', 6.5 * inch, 660, width=80, height=80)
        canvas.drawImage('RPA/footer.png', inch, 1, width=460, height=80)
        canvas.restoreState()

    def go():
        cliente = Cliente.objects.get(pk=cliente_id)
        doc = SimpleDocTemplate(buf, pagesize=letter,
                                rightMargin=inch, leftMargin=inch,
                                topMargin=2 * inch, bottomMargin=inch)
        encargado = cliente.encargado
        puesto = cliente.puesto_encargado
        clienteTexto = cliente.nombre

        Story = []

        styleN = styles["Normal"]
        styleH4 = styles["Heading4"]
        styleH2 = styles["Heading2"]

        styleRight = styles["Normal_R"]
        styleCB = styles[("Normal_CB")]
        styleB = styles[("Normal_B")]
        styleHB = styles[("Heading1_B")]
        styleHBC = styles[("Heading1_BC")]
        styleNC = styles[("Normal_C")]

        texto_fecha = ("Tijuana, B.C. a " + dateStr)
        texto_encargado = ("Attn. " + encargado)
        texto_asunto = ("Asunto:")

        p0 = Paragraph(texto_fecha, styleRight)
        p1 = Paragraph(texto_encargado, styleH4)
        p2 = Paragraph(puesto, styleN)
        p3 = Paragraph(clienteTexto, styleH2)
        p4 = Paragraph(texto_asunto, styleH2)
        p5 = Paragraph("""<u>"""+descripcion_cotizacion+"""</u>""", styleCB)
        p6 = Paragraph("Estimados señores, ", styleN)
        p7 = Paragraph("Según su solicitud, nos complace presentar la propuesta de mantenimiento, diagnóstico del sistema detección de incendios. en el documento, se especifican los requisitos generales para "+lugar_de_mantenimiento+" de "+nombre, styleN)
        pblank = Paragraph("""<para> <br/> </para>""")
        p8 = Paragraph("Índice de propuesta:, ", styleN)
        p9 = Paragraph("1.0 Fondo", styleN)
        p10 = Paragraph("2.0 Alcance de la descripción del trabajo", styleN)
        p11 = Paragraph("3.0 Resumen de propuestas económicas", styleN)
        p12 = Paragraph("4.0 Términos y condiciones", styleN)
        p13 = Paragraph("1.0 Fondo", styleHB)
        p14 = Paragraph("A continuación, se muestra una visión general de los equipos y condiciones actuales. Se presenta una lista de equipos instalados actualmente en el lugar.",styleN)
        p15 = Paragraph("1.1 Politica de mantenimiento preventivo",styleHB)
        p16 = Paragraph("Para aplicar el mantenimiento preventivo se entenderá que el sistema de detección de incendios debe estar en operación al 100%, si esto no se cumpliera así deberá realizarse primero el mantenimiento correctivo",styleN)
        p17 = Paragraph("Una politica de mantenimiento preventivo se considera valida para ",styleN)
        p18 = Paragraph("Vigencia **"+actyear+"-"+sigyear+"**",styleB)
        p19 = Paragraph("En la siguiente tabla se muestran las actividades que se consideran.",styleB)
        p20 = Paragraph("2.0 Alcance de la descripción del trabajo",styleHB)


        td_dispositivos =[["Marca","Nombre","Cantidad","Actvidad","Plan"]]
        dispositivos = cliente.dispositivo.all()
        for dispositivo in dispositivos:
            data_dispositivos = [dispositivo.marca,dispositivo.titulo,dispositivo.cantidad,dispositivo.actividad,dispositivo.plan]
            td_dispositivos.append(data_dispositivos)
        table_dis = Table(td_dispositivos)
        ts = TableStyle([("GRID",(0,0),(-1,-1),2,colors.black)])
        table_dis.setStyle(ts)

        td_mantenimientos = [["Mantenimiento","Acts. de mmnto por año","Acts. adicionales/Renta de equipo","Tiempo de ejecucion"]]
        mantenimientos = cliente.mantenimiento.all()
        for mantenimiento in mantenimientos:
            data_mantenimientos = [mantenimiento.title,mantenimiento.periodisidadactividades,mantenimiento.periodisidadadicional,mantenimiento.tiempoejecucion]
            td_mantenimientos.append(data_mantenimientos)
        table_man = Table(td_mantenimientos)
        table_man.setStyle(ts)

        td_total = [["Total de HRS de servicio de soporte técnico de poliza",""]]
        suma_horas = 0
        for mantenimiento in mantenimientos:
            suma_horas = +mantenimiento.tiempoejecucion

        data_mantenimientos = ["", suma_horas]
        td_total.append(data_mantenimientos)
        table_tot = Table(td_total)
        ts_tot = TableStyle([("GRID",(0,0),(-1,-1),2,colors.black),
                             ("BACKGROUND",(0,0),(-1,-1),colors.yellow)])
        table_tot.setStyle(ts_tot)

        ##Insertar variable de cliente precio aqui##

        td_precio = [["Description","QTY","Unit","Amount"]]
        data_precio = ["Cuota anual del contrato dde  mantenimiento", "1","Lot","$9713.98"]
        td_precio.append(data_precio)
        table_pre = Table(td_precio)
        ts_pre = TableStyle([("GRID",(0,0),(-1,-1),2,colors.black),
                             ("BACKGROUND",(0,0),(-1,0),colors.lightsteelblue)])
        table_pre.setStyle(ts_pre)

        p21 = Paragraph("3.0 Resumen de la propuesta económica",styleHB)
        p22 = Paragraph(actyear+"-"+sigyear+" Mantenimiento operativo regular y soporte técnico anual",styleB)

        p23 = Paragraph("Total de Propuesta Económica de Mantenimiento Preventivo",styleHBC)

        ptitulotermino = Paragraph("4.0 Términos y condiciones",styleHB)
        pterminos1 = Paragraph("Los precios cotizados se expresan en dólares americanos.",styleN,bulletText="-")
        pterminos2 = Paragraph("El IVA del 16% no está incluido.",styleN,bulletText="-")
        pterminos3 = Paragraph("El tipo de cambio será el de Santander a la venta en la ventanilla vigente el día de la operación de pago efectivo. LOS PAGOS NO SE ACEPTAN UTILIZANDO EL TIPO DE CAMBIO DEL DIARIO OFICIAL DE LA FEDERACIÓN.",styleN,bulletText="-")
        pterminos4 = Paragraph("Válido de la oferta: 30 días naturales, posteriormente los precios están sujetos a cambios sin previo aviso.",styleN,bulletText="-")
        pterminos5 = Paragraph("El proceso comienza confirmando su pago total o anticipo según sea el caso y su colocación del pedido de compra.",styleN,bulletText="-")
        pterminos6 = Paragraph("Para proceder con el mantenimiento correctivo, es necesario cubrir la póliza anual al 100% en el primer día de atención.",styleN,bulletText="-")
        pterminos7 = Paragraph("Para proceder con el mantenimiento preventivo, es necesario cubrir la anualidad de la póliza al 100% el primer día de la primera visita programada.",styleN,bulletText="-")
        pterminos8 = Paragraph("Los precios indicados son ofrecidos por el Total de la Propuesta aquí citado, cualquier cambio de condiciones o equipo seleccionado debe ser citado de nuevo.",styleN,bulletText="-")

        pfin = Paragraph("Fin del documento",styleNC)
        pregards = Paragraph("Regards",styleNC)
        pdanieljara = Paragraph("Ing. Daniel Jara Osuna",styleNC)
        pdirector = Paragraph("Director General",styleNC)

        Story.append(p0)
        Story.append(p1)
        Story.append(p2)
        Story.append(p3)
        Story.append(p4)
        Story.append(p5)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(p6)
        Story.append(pblank)
        Story.append(p7)
        Story.append(pblank)
        Story.append(p8)
        Story.append(p9)
        Story.append(p10)
        Story.append(p11)
        Story.append(p12)
        Story.append(PageBreak())

        #Segunda pagina
        Story.append(p13)
        Story.append(p14)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(table_dis)
        Story.append(PageBreak())

        #Tercera pagina
        Story.append(p15)
        Story.append(p16)
        Story.append(p17)
        Story.append(PageBreak())

        #Cuarta pagina
        Story.append(p18)
        Story.append(p19)
        Story.append(pblank)
        Story.append(table_man)
        Story.append(table_tot)
        Story.append(pblank)
        Story.append(PageBreak())

        #Quinta pagina
        Story.append(p20)
        Story.append(PageBreak())

        #Sexta pagina
        Story.append(p21)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(p22)
        Story.append(pblank)
        Story.append(table_pre)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(p23)

        Story.append(PageBreak())

        #Septima pagina
        Story.append(ptitulotermino)
        Story.append(pterminos1)
        Story.append(pterminos2)
        Story.append(pterminos3)
        Story.append(pterminos4)
        Story.append(pterminos5)
        Story.append(pterminos6)
        Story.append(pterminos7)
        Story.append(pterminos8)
        Story.append(pblank)
        Story.append(pfin)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pregards)
        Story.append(pdanieljara)
        Story.append(pdirector)





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
