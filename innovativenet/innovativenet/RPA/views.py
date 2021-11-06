from django.utils.translation import templatize
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table,TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.rl_config import defaultPageSize
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from django.http import FileResponse
from django.urls import reverse
from reportlab.pdfgen import canvas
from django.contrib import messages
from reportlab.lib import colors
from datetime import datetime
from .models import *
from datetime import date
import io
import os
from pathlib import Path
from operator import itemgetter
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from num2words import num2words


class CustomLoginView(LoginView):
    # Esta clase se encarga de verificar que el usuario este autenticado antes de poder
    # entrar a cualquier parte de la pagina.
    template_name = 'mantenimientos/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return reverse_lazy('lista_clientes')


class Home(LoginRequiredMixin, ListView):
    model = Cliente
    context_object_name = 'Cliente'
    template_name = 'mantenimientos/home.html'
    # Se encarga de manejar los datos observables por el usuario

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # compara los usuarios con su informacion y projecta solo informacion de usuario
        context['Cliente'] = context['Cliente'].filter(
            usuario=self.request.user)
        #context['count'] = context['mantenimientos'].filter(complete=False).count()
        return context


# ------ VIEWS COTIZACION ------ #

class Agregar_Cotizacion(LoginRequiredMixin, CreateView):
    model = Cotizacion
    fields = ['titulo', 'lugar_de_mantenimiento', 'descripcion_cotizacion','periodoregular','preguntaperiodoadicional','periodoadicional']
    template_name = 'cotizacion/agregar_cotizacion.html'

    def form_valid(self, form):
        form.instance.cliente = Cliente.objects.get(pk=self.kwargs['cliente'])
        return super(Agregar_Cotizacion, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('mostrar_cliente', kwargs={'pk':self.object.cliente.id})

class Detalle_Cotizacion(LoginRequiredMixin, DetailView):
    model = Cotizacion
    object = "cotizacion"
    template_name = "cotizacion/detalle_cotizacion.html"
    def get_context_data(self, **kwargs):
        ctx = super(Detalle_Cotizacion, self).get_context_data(**kwargs)
        # del diccionario de Key Word ARGumentS obtiene el valor de object
        cat = kwargs.get("object")
        ctx['servicios'] = Mantenimiento.objects.filter(cotizacion = cat)
        return ctx
        
class Modificar_Cotizacion(LoginRequiredMixin, UpdateView):
    model = Cotizacion
    object = "cotizacion"
    fields = ['titulo', 'lugar_de_mantenimiento', 'descripcion_cotizacion']
    template_name = 'cotizacion/modificar_cotizacion.html'
    def get_success_url(self):
        return reverse('mostrar_cliente', kwargs={'pk':self.object.cliente.id})

class Eliminar_Cotizacion(LoginRequiredMixin, DeleteView):
    model = Cotizacion
    context_object_name = "cotizacion"
    template_name = "cotizacion/eliminar_cotizacion.html"

    def get_success_url(self):
        return reverse('mostrar_cliente', kwargs={'pk':self.object.cliente.id})


# ------ VIEWS DISPOSITIVOS ------ #

class Agregar_Dispositivo(LoginRequiredMixin, CreateView):
    # Manda a llamar el Modelo Mantenimiento
    model = Dispositivo
    # Hace la eleccion de que inputs del Modelo tomar en cuenta
    fields = ['titulo','cantidad','actividad','plan']
    # Se utiliza para regresar al usuario a una pagina en especifico despues de terminar
    success_url = reverse_lazy('lista_clientes')
    # Busca un html en especifico
    template_name = 'dispositivos/agregar_dispositivo.html'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.cliente = Cliente.objects.get(pk=self.kwargs['pk'])
        return super(Agregar_Dispositivo, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('Mostrar_Cliente', kwargs={'pk': self.object.cliente.id})


class Update_Dispositivo(LoginRequiredMixin, UpdateView):
    model = Dispositivo
    fields =['marca','titulo','cantidad','actividad','plan']
    template_name = 'dispositivos/modificar_dispositivo.html'
    def get_success_url(self):
        return reverse('mostrar_cliente', kwargs={'pk':self.object.cliente.id})


class Eliminar_Dispositivo(LoginRequiredMixin, DeleteView):
    model = Dispositivo
    context_object_name = 'dispositivo'
    template_name = 'dispositivos/eliminar_dispositivo.html'
    def get_success_url(self):
        return reverse('mostrar_cliente', kwargs={'pk':self.object.cliente.id})


class Detalle_Dispositivo(LoginRequiredMixin, DetailView):
    model = Dispositivo
    context_object_name = 'dispositivo'
    template_name = 'dispositivos/detalle_dispositivo.html'

# ------ VIEWS SERVICIOS ------ #

class Agregar_Mantenimiento(LoginRequiredMixin, CreateView):
    # Manda a llamar el Modelo Mantenimiento
    model = Mantenimiento
    # Hace la eleccion de que inputs del Modelo tomar en cuenta
    fields = ['titulonombre', 'periodisidadactividades', 'periodisidadadicional',
                'cantidaddedispositivos', 'cantidaddispositivosextras',
                ]
    # Busca un html en especifico
    template_name = 'mantenimientos/agregar_servicio.html'

    # Cuando se confirma el mantenimiento
    def form_valid(self, form):
        # se agrega el usuario que se esta usando en la instancia de usuario
        form.instance.cliente = Cliente.objects.get(pk=self.kwargs['cliente'])
        form.instance.cotizacion = Cotizacion.objects.get(pk=self.kwargs['pk'])
        return super(Agregar_Mantenimiento, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('detalle_cotizacion', kwargs={'pk':self.object.cotizacion.id,'cliente':self.object.cotizacion.cliente.id})

class MttoUpdate(LoginRequiredMixin, UpdateView):
    model = Mantenimiento
    fields = ['titulonombre','periodisidadactividades', 'periodisidadadicional','cantidaddedispositivos', 'cantidaddispositivosextras',]
    template_name = 'mantenimientos/modificar_servicio.html'

    def get_success_url(self):
        return reverse('detalle_cotizacion', kwargs={'pk':self.object.cotizacion.id,'cliente':self.object.cotizacion.cliente.id})



class EliminarMantenimiento(LoginRequiredMixin, DeleteView):
    model = Mantenimiento
    context_object_name = 'servicio'
    template_name = 'mantenimientos/eliminar_servicio.html'
    
    def get_success_url(self):
        return reverse('detalle_cotizacion', kwargs={'cliente':self.object.cotizacion.cliente.id,'pk':self.object.cotizacion.id})


class Detalle_Servicio(LoginRequiredMixin, DetailView):
    model = Mantenimiento
    context_object_name = 'servicio'
    template_name = 'mantenimientos/detalle_servicio.html'

# ------ VIEWS CLIENTE ------ #

class Agregar_Cliente(LoginRequiredMixin, CreateView):
    model = Cliente
    fields = ['nombre', 'encargado', 'puesto_encargado', 
            'numero_contacto', 'correo_contacto',]
    success_url = reverse_lazy('lista_clientes')
    template_name = 'cliente/agregar_cliente.html'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(Agregar_Cliente, self).form_valid(form)
    def get_success_url(self):
        return reverse('mostrar_cliente', kwargs={'pk':self.object.pk})


class Modificar_Cliente (LoginRequiredMixin, UpdateView):
    model = Cliente
    fields = ['nombre', 'encargado', 'puesto_encargado',
              'numero_contacto', 'correo_contacto', ]
    success_url = reverse_lazy('lista_clientes')
    template_name = 'cliente/modificar_cliente.html'
    def get_success_url(self):
        return reverse('mostrar_cliente', kwargs={'pk': self.object.pk})

class Eliminar_Cliente(LoginRequiredMixin, DeleteView):
    model = Cliente
    context_object_name = "cliente"
    success_url = reverse_lazy("lista_clientes")
    template_name = "cliente/eliminar_cliente.html"

# Esta clase se encarga de visualizar los clientes de cada usuario
class Todos_Clientes(LoginRequiredMixin, ListView):
    model = Cliente
    context_object_name = 'lista_clientes'
    template_name = 'cliente/lista_clientes.html'
    # Se encarga de manejar los datos observables por el usuario
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # compara los usuarios con su informacion y projecta solo informacion de usuario
        context['lista_clientes'] = context['lista_clientes'].filter(usuario=self.request.user)
        #context['count'] = context['mantenimientos'].filter(complete=False).count()
        return context



def buscar_clientes(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        clientes = Cliente.objects.filter(nombre__contains=searched)
        return render(request,
                      'mantenimientos/buscar_clientes.html',
                      {'searched':searched,
                       'clientes':clientes,
                       })
    else:
        return render(request, 'cliente/buscar_clientes.html',{})


class Mostrar_Cliente(LoginRequiredMixin, DetailView):
    model = Cliente
    object = "cliente"
    template_name = "cliente/detalle_cliente.html"
    def get_context_data(self, **kwargs):
        ctx = super(Mostrar_Cliente, self).get_context_data(**kwargs)
        # del diccionario de Key Word ARGumentS obtiene el valor de object
        cat = kwargs.get("object")
        # filtra los elemento de la clase y los determina en
        # el html con el nombre dado en ctx['cotizaciones']
        ctx['cotizaciones'] = Cotizacion.objects.filter(cliente = cat)
        return ctx






# --------- DESCARGA PDF ----------------------------

def cotizacion_pdf(request, cliente_id):

    cliente = Cliente.objects.get(pk=cliente_id)
    # mantenimientos = Cliente.mantenimiento.through.objects.
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
    styles.add(ParagraphStyle(name='Normal_Right',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_RIGHT,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
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
    styles.add(ParagraphStyle(name='Normal_Red',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_LEFT,
                              fontSize=12,
                              textColor=colors.red,
                              fontName="Helvetica-bold",
                              ))
    styles.add(ParagraphStyle(name='Normal_Ye',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              backColor = colors.yellow,
                              ))


    def myFirstPage(canvas, doc):
        BASE_DIR = Path(__file__).resolve().parent.parent
        canvas.saveState()
        canvas.setFont('Times-Bold', 16)
        canvas.setFont('Times-Roman', 14)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','logo.png'), 0.8 * inch, 660, width=160, height=80)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','lenellogo.png'), 6.5 * inch, 660, width=80, height=80)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','footer.png'), inch, 1, width=460, height=80)
        canvas.restoreState()

    def myLaterPages(canvas, doc):
        BASE_DIR = Path(__file__).resolve().parent.parent
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','logo.png'), 0.8 * inch, 660, width=160, height=80)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','lenellogo.png'), 6.5 * inch, 660, width=80, height=80)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','footer.png'), inch, 1, width=460, height=80)
        canvas.restoreState()

    def go():
        cliente = Cliente.objects.get(pk=cliente_id)
        mantenimientos = Mantenimiento.objects.filter(cliente = cliente_id)
        dispositivos = Dispositivo.objects.filter(cliente = cliente_id)
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
        styleNR = styles[("Normal_Red")]
        styleNY = styles[("Normal_Ye")]
        styleNRight = styles[("Normal_Right")]

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
        listadispositivos = ''
        listdisp = list(dispositivos)
        lastdisp = listdisp[-1]
        
        for dispositivo in dispositivos:
            if len(dispositivos) == 1:
                listadispositivos = listadispositivos+" "+str(dispositivo.cantidad)+" "+str(dispositivo.titulo)+'.'
            
            elif dispositivo != lastdisp:
                listadispositivos = listadispositivos+" "+str(dispositivo.cantidad)+" "+str(dispositivo.titulo)+","
                
            elif dispositivo == lastdisp:
                listadispositivos = listadispositivos+" "+str(dispositivo.cantidad)+" "+str(dispositivo.titulo)+","
                listadispositivos = listadispositivos[:-1]
                listadispositivos = listadispositivos+"."


            
        p17 = Paragraph("Una politica de mantenimiento preventivo se considera valida para "+str(listadispositivos),styleN)
        p18 = Paragraph("Vigencia **"+actyear+"-"+sigyear+"**",styleB)
        p19 = Paragraph("En la siguiente tabla se muestran las actividades que se consideran.",styleB)
        p20 = Paragraph("2.0 Alcance de la descripción del trabajo",styleHB)
        palcances1 = Paragraph("Cada actividad de servicio de 1 año",styleNR)
        palcances2 = Paragraph("Limpieza de dispositivos 12-20 pies de altura.",styleN,bulletText="•")
        palcances3 = Paragraph("Limpieza de Panel (Pantallas lcd, conectores, terminales de cableado, limpieza,sellos silicón, limpiezageneral del Panel en sus partes de funcionalidad revisión de conectividad a panel o y actividad en lazo)",styleN,bulletText="•")
        palcances4 = Paragraph("Limpieza del sistema de gestión de energía exterior (filtros de aire, CSI· C., sellos de silicona de gabinete, conectores de conducto de ajuste, fuente de alimentación, baterías, cables de alimentación y conectores).",styleN,bulletText="•")
        palcances5 = Paragraph("Revisión de la comunicación de dispositivos con el PANEL",styleN,bulletText="•")
        palcances6 = Paragraph("Comprobar el funcionamiento de las fuentes de alimentación",styleN,bulletText="•")
        palcances7 = Paragraph("Verificar la prueba del lazo",styleN,bulletText="•")
        palcances8 = Paragraph("De forma programada, cada 1er día laborable de cada mes se limpiará el equipo antes mencionado.",styleN,bulletText="•")

        palcances9 = Paragraph("Monitoreo de revisiones de los puntos anteriores.",styleN,bulletText="•")
        palcances10 = Paragraph("Servicio profesional para aplicar los conocimientos de ingeniería especializada en Detección de incendios",styleN,bulletText="•")
        palcances11= Paragraph("De forma programada, una vez al año el equipo mencionado anteriormente se realizará el mmtto Preventivo. En caso de fallos en el sistema se propondrá realizar el Mmtto Correctivo ",styleN,bulletText="•")
        palcances12= Paragraph("El alcance es sólo para el sistema de detección de incendios, Panel y equipos instalados previamente en sitio mencionado en esta propuesta en la sección inicial fondo de este documento",styleN,bulletText="•")
        palcances13= Paragraph("Una vez completado el mantenimiento, el informe se entrega con la información resultante, el formato que especifica el estado actual de cada equipo.",styleN,bulletText="•")
        palcances14= Paragraph("El informe hará la recomendación de corrección, reparación o sustitución de cualquiera de los equipos.",styleN,bulletText="•")
        palcances15= Paragraph("El pago del mantenimiento es anual, debe ser pagado antes de ser realizado.",styleN,bulletText="•")
        palcances16= Paragraph("Incluye Maquinaria de elevacion.",styleN,bulletText="•")

        ppolitica = Paragraph("2.1 Política de apoyo técnico y diagnóstico",styleHB)
        ppolitica1 = Paragraph("Teléfono móvil disponible para emergencias durante las horas contratadas.",styleN,bulletText="•")
        ppolitica2 = Paragraph("Soporte técnico telefónico con un tiempo de respuesta de 4 horas.",styleN,bulletText="•")
        ppolitica3 = Paragraph("Soporte técnico in situ 4 horas de tiempo de respuesta, 5 días a la semana (de lunes a viernes de 8:00am a 5:00pm).",styleN,bulletText="•")
        ppolitica4 = Paragraph("30 (treinta) horas de servicio técnico incluyen por un período de 12 meses, Si el cliente hace uso de las 30 hrs de servicio, deberá renovarse la Póliza en una nueva cotización",styleN,bulletText="•")
        ppolitica5 = Paragraph("El alcance es sólo para el sistema de detección de incendios, hardware de DCI mencionado en esta propuesta en la sección inicial fondo de este documento",styleN,bulletText="•")
        ppolitica6 = Paragraph("Para la atención de:",styleN,bulletText="•")
        ppolitica7 = Paragraph("Fallos y diagnóstico",styleN,bulletText="-")
        ppolitica8 = Paragraph("Ajustes",styleN,bulletText="-")
        ppolitica9 = Paragraph("Actualizaciones",styleN,bulletText="-")
        ppolitica10 = Paragraph("Panel, configuraciones de equipo de detección",styleN,bulletText="-")
        ppolitica11 = Paragraph("Soporte técnico para problemas con el Panel",styleN,bulletText="-")
        ppolitica12 = Paragraph("Soporte técnico para problemas con los dispositivos",styleN,bulletText="-")
        ppolitica13 = Paragraph("Tarjetas loops, panel, estrobos, sensores fotoeléctricos, fuentes de poder, módulos de control. Monitores de flujo, resistencias de fin de línea.",styleN,bulletText="-")
        ppolitica14 = Paragraph("Emergencias del sistemas (1 hora)",styleN,bulletText="-")
        ppolitica15 = Paragraph("Si se detecta un dispositivo dañado durante el diagnóstico, se notificará en el relleno de informe para su posterior mmtto correctivo. ",styleN,bulletText="•")
        ppolitica16 = Paragraph("""<u>Sistema base web para mejorar sus servicios y registros de mantenimiento</u>""",styleN,bulletText="•")




        td_dispositivos =[["Nombre","Cantidad","Plan"]] 
        for dispositivo in dispositivos:
            data_dispositivos = [dispositivo.titulo,dispositivo.cantidad,dispositivo.plan]
            td_dispositivos.append(data_dispositivos)
        table_dis = Table(td_dispositivos)
        ts = TableStyle([("GRID",(0,0),(-1,-1),2,colors.black)])
        table_dis.setStyle(ts)

        td_mantenimientos = [["Mantenimiento","Acts. de mmnto por año",
                            "Acts. adicionales/Renta de equipo"
                            ,"Tiempo de ejecucion"]]
        for mantenimiento in mantenimientos:
            data_mantenimientos = [mantenimiento.Titulo,mantenimiento.periodisidadactividades,mantenimiento.periodisidadadicional,mantenimiento.tiempoejecucion]
            td_mantenimientos.append(data_mantenimientos)
        table_man = Table(td_mantenimientos)
        table_man.setStyle(ts)

        td_total = [["Total de HRS de servicio de soporte técnico de poliza",""]]
        suma_horas = 0
        for mantenimiento in mantenimientos:
            suma_horas = suma_horas + mantenimiento.horasactividad

        data_mantenimientos = ["", suma_horas]
        td_total.append(data_mantenimientos)
        table_tot = Table(td_total)
        ts_tot = TableStyle([("GRID",(0,0),(-1,-1),2,colors.black),
                             ("BACKGROUND",(0,0),(-1,-1),colors.yellow)])
        table_tot.setStyle(ts_tot)

        preciofinal = 0
        for mantenimiento in mantenimientos:
            preciofinal = preciofinal + mantenimiento.costomantenimientoregular
        preciofinal = float(round(preciofinal))
        preciofinal1 = num2words(preciofinal, to="currency", lang='es', currency='USD').upper()
        
        td_precio = [["Description","QTY","Unit","Amount"]]
        data_precio = ["Cuota anual del contrato de  mantenimiento", "1","Lot","${}".format(preciofinal)]
        td_precio.append(data_precio)
        table_pre = Table(td_precio)
        ts_pre = TableStyle([("GRID",(0,0),(-1,-1),2,colors.black),
                             ("BACKGROUND",(0,0),(-1,0),colors.lightsteelblue)])
        table_pre.setStyle(ts_pre)
        ppreciotexto = Paragraph(preciofinal1+" USD + IVA",styleNRight)
        p21 = Paragraph("3.0 Resumen de la propuesta económica",styleHB)
        p22 = Paragraph(actyear+"-"+sigyear+" Mantenimiento operativo regular y soporte técnico anual",styleB)


        p23 = Paragraph("Total de Propuesta Económica de Mantenimiento Preventivo",styleHBC)
        p24 = Paragraph("Mmto.....................................................${}".format(preciofinal),styleNY)
        p25 = Paragraph(preciofinal1+" USD + IVA",styleNY)
        p26 = Paragraph("**Incluye maquinaria de elevacion**",styleCB)

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
        Story.append(pblank)
        Story.append(palcances1)
        Story.append(pblank)
        Story.append(palcances2)
        Story.append(palcances3)
        Story.append(palcances4)
        Story.append(palcances5)
        Story.append(palcances6)
        Story.append(palcances7)
        Story.append(palcances8)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(palcances1)
        Story.append(pblank)
        Story.append(palcances9)
        Story.append(palcances10)
        Story.append(palcances11)
        Story.append(palcances12)
        Story.append(palcances13)
        Story.append(palcances14)
        Story.append(palcances15)
        Story.append(palcances16)
        Story.append(pblank)

        Story.append(PageBreak())


        Story.append(ppolitica)
        Story.append(ppolitica1)
        Story.append(ppolitica2)
        Story.append(ppolitica3)
        Story.append(ppolitica4)
        Story.append(ppolitica5)
        Story.append(ppolitica6)
        Story.append(ppolitica7)
        Story.append(ppolitica8)
        Story.append(ppolitica9)
        Story.append(ppolitica10)
        Story.append(ppolitica11)
        Story.append(ppolitica12)
        Story.append(ppolitica13)
        Story.append(ppolitica14)
        Story.append(ppolitica15)
        Story.append(ppolitica16)


        Story.append(PageBreak())

        #Sexta pagina
        Story.append(p21)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(p22)
        Story.append(pblank)
        Story.append(table_pre)
        Story.append(ppreciotexto)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(p23)
        Story.append(p24)
        Story.append(p25)
        Story.append(p26)


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
    return FileResponse(buf, as_attachment=True,  filename='cotizacion.pdf')



# Create your views here.
