from django.utils.translation import templatize
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle, Indenter
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
        return reverse('detalle_cotizacion', kwargs={'cliente':self.object.cliente.pk, 'pk':self.object.pk})

class Detalle_Cotizacion(LoginRequiredMixin, DetailView):
    model = Cotizacion
    object = "cotizacion"
    template_name = "cotizacion/detalle_cotizacion.html"
    def get_context_data(self, **kwargs):
        ctx = super(Detalle_Cotizacion, self).get_context_data(**kwargs)
        # del diccionario de Key Word ARGumentS obtiene el valor de object
        cat = kwargs.get("object")
        ctx['servicios'] = Mantenimiento.objects.filter(cotizacion = cat)
        ctx['servicios'] = ctx['servicios'].exclude(titulonombre=Nombre_servicio.objects.get(pk=13))
        ctx['servicios'] = ctx['servicios'].exclude(encargadoTrabajo1=Precio.objects.get(encargado='Ingeniero'))
        ctx['serviciosplus'] = Mantenimiento.objects.filter(cotizacion = cat,titulonombre=Nombre_servicio.objects.get(pk=16))

        #ctx['']
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
    context_object_name = 'servicio'
    fields = ['periodisidadactividades', 'periodisidadadicional','cantidaddedispositivos', 'cantidaddispositivosextras','tiempoejecucion']
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

def cotizacion_pdf(request, cliente_id,cotizacion_id,usuario):

    cliente = Cliente.objects.get(pk=cliente_id)
    cotizacion = Cotizacion.objects.get(pk=cotizacion_id,cliente=cliente_id)
    # mantenimientos = Cliente.mantenimiento.through.objects.
    buf = io.BytesIO()

    nombre=cliente.nombre
    encargado=cliente.encargado
    puesto_encargado = cliente.puesto_encargado
    numero_contacto = cliente.numero_contacto
    correo_contacto = cliente.correo_contacto
    lugar_de_mantenimiento = cotizacion.lugar_de_mantenimiento
    descripcion_cotizacion = cotizacion.descripcion_cotizacion
    fecha = cotizacion.fecha

    dateTimeObj = datetime.now()
    dateObj = dateTimeObj.date()
    dateStr = dateObj.strftime("%b %d , %Y")

    actyear = str(date.today().year)
    sigyear = str(date.today().year + 1)

    PAGE_HEIGHT = defaultPageSize[1]
    PAGE_WIDTH = defaultPageSize[0]
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Normal_R',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_RIGHT,
                              fontSize=12,
                              textColor=colors.black,
                              ))
    styles.add(ParagraphStyle(name='Normal_J',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_JUSTIFY,
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
    styles.add(ParagraphStyle(name='Normal_Center',
                            parent=styles['Normal'],
                            wordWrap='CJK',
                            alignment=TA_CENTER,
                            fontSize=12,
                            textColor=colors.black,
                            fontName="Helvetica-bold",
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
        mantenimientos = Mantenimiento.objects.filter(cliente = cliente_id,cotizacion=cotizacion_id)
        for mantenimiento in mantenimientos:
            listdisp = []
            listdisp.append(mantenimiento.dispositivo)
        cliente = Cliente.objects.get(pk=cliente_id)
        cotizacion = Cotizacion.objects.get(pk=cotizacion_id,cliente=cliente_id)
        doc = SimpleDocTemplate(buf, pagesize=letter,
                                rightMargin=inch, leftMargin=inch,
                                topMargin=2 * inch, bottomMargin=inch)
        encargado = cliente.encargado
        puesto = cliente.puesto_encargado
        clienteTexto = cliente.nombre

        Story = []

        styleN = styles["Normal"]
        styleN = styles["Normal_J"]
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
        styleNBC = styles[("Normal_Center")]
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
        p7 = Paragraph("En relación con su solicitud nos complace presentar la propuesta de mantenimiento del sistema de detección de incendios, en este documento se presenta la propuesta económica basados en las características de su edificio y sus equipos actuales en la compañía "+nombre+" ubicada en la ciudad de "+lugar_de_mantenimiento, styleN)
        pblank = Paragraph("""<para> <br/> </para>""")
        p8 = Paragraph("Índice de propuesta:, ", styleN)
        p9 = Paragraph("1.0 Fondo", styleN)
        p10 = Paragraph("2.0 Alcance de la descripción del trabajo", styleN)
        p11 = Paragraph("3.0 Resumen de propuestas económicas", styleN)
        p12 = Paragraph("4.0 Términos y condiciones", styleN)
        p13 = Paragraph("1.0 Fondo", styleHB)
        p14 = Paragraph("A continuación en la tabla de abajo se muestra una visión general de los equipos , así como las visitas de mantenimiento anual consideradas en un año calendario, la columna cantidad indica el numero de dispositivos considerados a mantener en esta oferta económica de cada tipo de manera regular en base ya sea a nuestras recomendación o a las políticas de seguridad establecidas por el cliente.",styleN)
        p1extra = Paragraph("Regularmente las visitas adicionales por año son aquellas visitas que proponemos realizar adicional a las visitas regulares  ya sea porque están sujetas a condiciones de clima, polvos, suciedad o químicos fuera de lo normal, pueden dispositivos en áreas en construcciones remodelaciones o presencia de químicos, si la columna esta en “0” esto significa que no se esta considerando ninguna zona como anteriormente se explica.",styleN)
        p15 = Paragraph("1.1 Politica de mantenimiento preventivo",styleHB)
        p16 = Paragraph("Para proceder y aplicar un mantenimiento preventivo se entiende que el sistema de detección de incendios debe estar en operación al 100% sin ninguna falla o problema, si este no cumple deberá de realizarse primero un mantenimiento correctivo bajo presupuesto adicional que no forma parte de este presupuesto.",styleN)
        p2extra = Paragraph("El mantenimiento preventivo considera un compromiso de la empresa para la ejecución de una serie de acciones a el panel y dispositivos de manera calendarizada bajo una fecha establecida con la finalidad de mantener la operación del sistema al 100% funcional desde el inicio de la fecha de contrato hasta 365 días después de la firma del mismo.",styleN)
        listdisp = [["Dispositivo","Cantidad",Paragraph("Visitas por año"),Paragraph("Visitas adicionales por año"),Paragraph("Dispositivos en periodicidad adcional")]]
        mantenimientos = Mantenimiento.objects.filter(cliente = cliente_id,cotizacion=cotizacion_id)
        for mantenimiento in mantenimientos:
            if mantenimiento.periodisidadadicional is not None or mantenimiento.periodisidadadicional != 0:
                if mantenimiento.dispositivo is not None:
                    if mantenimiento.periodisidadadicional is None:
                        info_disp = [mantenimiento.dispositivo,mantenimiento.cantidaddedispositivos,mantenimiento.periodisidadactividades,0,0]
                    else:    
                        info_disp = [mantenimiento.dispositivo,mantenimiento.cantidaddedispositivos,mantenimiento.periodisidadactividades,mantenimiento.periodisidadadicional,mantenimiento.cantidaddispositivosextras]
                    listdisp.append(info_disp)
            else:
                if mantenimiento.dispositivo is not None:
                    info_disp = [mantenimiento.dispositivo,mantenimiento.cantidaddedispositivos]
                    listdisp.append(info_disp)

        listadispositivos = ''
        lastdisp = listdisp[-1]

        for mantenimiento in mantenimientos:
            if len(listdisp) == 1:
                if mantenimiento.dispositivo is not None:
                    listadispositivos = listadispositivos+" "+str(mantenimiento.cantidaddedispositivos)+" "+str(mantenimiento.dispositivo)+'.'
            
            elif mantenimiento.dispositivo != lastdisp:
                if mantenimiento.dispositivo is not None:
                    listadispositivos = listadispositivos+" "+str(mantenimiento.cantidaddedispositivos)+" "+str(mantenimiento.dispositivo)+","
                
            else:
                if mantenimiento.dispositivo is not None:
                    listadispositivos = listadispositivos+" "+str(mantenimiento.cantidaddedispositivos)+" "+str(mantenimiento.dispositivo)+","
                    listadispositivos = listadispositivos[:-1]
                    listadispositivos = listadispositivos+"."

        titulo = Nombre_servicio.objects.get(pk=13)
        totaldisp = Mantenimiento.objects.get(titulonombre = titulo,cotizacion=cotizacion_id,cliente=cliente_id)
        p17 = Paragraph("Se considera dentro de los dispositivos a mantener el equipo que actualmente cuentan considerándose "+str(listadispositivos),styleN)
        p3extra = Paragraph("Total de dispositivos: "+str(totaldisp.cantidaddedispositivos), styleN)
        p4extra = Paragraph("La maquinaria de elevación es necesaria utilizarse en dispositivos mas de 15 pies de altura, este tipo de equipo tienen un costo asociado por su traslado al sitio y recolección, su uso por día y es necesario recargarse bajo una toma eléctrica, esta maquinaria de elevación no esta considerada en su costo, por lo que queda por responsabilidad del cliente solicitar una de ser necesaria para este trabajo de mantenimiento en las visitas que sean necesaria de una manera programada, así como las facilidades eléctricas para la recarga del equipo.",styleN)
        p18 = Paragraph("Periodo de cobertura "+actyear+"-"+sigyear,styleB)
        p19 = Paragraph("En la siguiente tabla se muestran las actividades que se consideran.",styleB)
        p20 = Paragraph("2.0 Alcance de la descripción del trabajo",styleHB)
        p5extra = Paragraph("Que se Incluye en esta póliza de mantenimiento del sistema de detección de fuego?: ",styleB)
        if cotizacion.periodoregular == 1:
            palcances1= Paragraph(str(cotizacion.periodoregular)+" visita de actividades de mantenimiento al año.",styleN,bulletText="•")
        else:
            palcances1= Paragraph(str(cotizacion.periodoregular)+" visitas de actividades de mantenimiento al año.",styleN,bulletText="•")
        ppolitica16 = Paragraph("Disponibilidad de portal WEB personalizado para el seguimiento por personal asignado del cliente con todo el Equipo técnico de la empresa para visualización de las actividades de mantenimiento y reportes.",styleN,bulletText="•")
        palcances2 = Paragraph("Poner el sistema en modo de prueba.",styleN,bulletText="•")
        palcances3 = Paragraph("De manera calendarizada cada Visita  se ejecutara la limpieza de los sensores y módulos físicamente. Los dispositivos para limpiar dando mayor jerarquía  son los que determine el reporte de mantenimiento y sensibilidad que indique un nivel de suciedad mayor al 35% después se procede con el resto.",styleN,bulletText="•")
        palcances4 = Paragraph("Limpieza de panel de alarmas ( pantalla LCD, conectores, terminales de cableado, limpieza, sellos silicón, revisión de conectividad a panel remoto y actividad en el Lazo SLC de dispositivos).",styleN,bulletText="•")
        palcances5 = Paragraph("Reporte de sensibilidad el cual nos indica que sensor está sucio de sus elementos internos para proceder a limpiarlos.",styleN,bulletText="•")
        palcances6 = Paragraph("Limpieza de estrobos-cornetas y palancas.",styleN,bulletText="•")
        palcances7 = Paragraph("Prueba de verificación de leds del panel , iluminar todos los leds.",styleN,bulletText="•")
        palcances8 = Paragraph("Prueba de verificación de energía primaria, remover energía de AC, verificar que el panel funcione con baterías, verificar que el panel entre en modo de problema, restablecer energía y dejar todo en orden en modo normal.",styleN,bulletText="•")

        palcances9 = Paragraph("Prueba de señales de problema en panel  funcionen apropiadamente",styleN,bulletText="•")
        palcances10 = Paragraph("Verificación bimestral que la pantalla LCD del panel marque la hora apropiada.",styleN,bulletText="•")
        p6extra = Paragraph("""<u>¿Que no se incluye?:</u>""",styleB)

        
        palcances12= Paragraph("Equipos y Refacciones.",styleN,bulletText="1.")
        palcances13= Paragraph("Materiales como cables o tuberías.",styleN,bulletText="2.")
        palcances14= Paragraph("Maquinaria de elevación.",styleN,bulletText="3.")
        palcances15= Paragraph("Trabajos en días Festivos",styleN,bulletText="4.")
        palcances16= Paragraph("Trabajos fuera del horario establecido.",styleN,bulletText="5.")
        suma_horas = 0
        for mantenimiento in mantenimientos:
            if str(mantenimiento.titulonombre) == "Servicio de soporte técnico -Horas de servicios generales adicionales":
                suma_horas = mantenimiento.tiempoejecucion
        suma_horas_palabra = num2words(suma_horas,lang='es')
        

        ppolitica = Paragraph("2.1 Política de apoyo técnico y diagnóstico",styleHB)
        ppoliticaextra1=Paragraph("""<u>¿Que se Incluye en las horas de Servicios de soporte Técnico, pruebas y servicios de reparación consideradas en esta propuesta?:</u>""",styleB)
        ppolitica1 = Paragraph("Servicio de soporte técnico para diagnostico o corrección por "+str(suma_horas)+" horas o 12 meses, lo que suceda primero.  ",styleN,bulletText="•")
        ppolitica2 = Paragraph("Días regular para Soporte técnico de Lunes a sábado (horarios de 8.00am – 6:00pm)",styleN,bulletText="•")
        ppolitica3 = Paragraph("Atención técnica y reparación de fallas en los paneles o en los dispositivos en su red.",styleN,bulletText="•")
        ppolitica4 = Paragraph("Tiempo de respuesta de servicios normal: siguiente día hábil.",styleN,bulletText="•")
        ppolitica5 = Paragraph("Prueba semestral de palancas manuales, inspección visual, activar el mecanismo y confirmar respuesta en la zona apropiada.",styleN,bulletText="•")
        ppolitica6 = Paragraph("Prueba semestral de detectores de calor, inspección visual, conducir una función de prueba para verificar la respuesta en la zona apropiada.",styleN,bulletText="•")
        ppolitica7 = Paragraph("Prueba anual de detectores de humo, conducir una función de prueba para verificar la respuesta en la zona apropiada.",styleN,bulletText="•")
        ppolitica8 = Paragraph("Prueba semestral de todos los dispositivos de iniciación de alarmas, activar los dispositivos y verificar que los circuitos de aplicación de notificación apropiados estén funcionando correctamente (NAC) así como información de zona y mensajes correspondientes, abrir el cableado de campo de los dispositivos de iniciación y verificar que el mensaje de problema se indique en el panel.",styleN,bulletText="•")
        ppolitica9 = Paragraph("Prueba anual de Notificación en cornetas-estrobos, colocar el panel en alarma, drill o modo de prueba y verificar que todos los notificadores estén trabajando apropiadamente.",styleN,bulletText="•")
        ppolitica10 = Paragraph("Prueba de energía secundaria en los paneles principales y remotos, remover energía primaria de AC, medir corrientes en modo “stand by” y  alarmado y comparar con cálculo de baterías para verificar una capacidad de batería adecuada, probar a plena carga por 5 minutos, medir voltajes de baterías a plena carga, restablecer energía primaria de AC al final de la prueba, restablecer y cerrar panel al final de la prueba.",styleN,bulletText="•")
        ppolitica11 = Paragraph("Mano de obra por remplazo de cualquier refacción como módulos, sensores, tarjetas, paneles, fuentes de poder, cables",styleN,bulletText="•")
        listadispositivospol = ''
        lastdisppol = listdisp[-1]

        for mantenimiento in mantenimientos:
            if len(listdisp) == 1:
                if mantenimiento.dispositivo is not None:
                    listadispositivospol = listadispositivospol+" "+str(mantenimiento.dispositivo)+'.'
            
            elif mantenimiento.dispositivo != lastdisppol:
                if mantenimiento.dispositivo is not None:
                    listadispositivospol = listadispositivospol+" "+str(mantenimiento.dispositivo)+","
                
            else:
                if mantenimiento.dispositivo is not None:
                    listadispositivospol = listadispositivos+" "+str(mantenimiento.dispositivo)+","
                    listadispositivospol = listadispositivospol[:-1]
                    listadispositivospol = listadispositivospol+"."


        ppolitica12 = Paragraph("Tiempo de  Programación y configuración de Paneles  sobre los equipos dentro de la póliza de mantenimiento.",styleN,bulletText="•")
        #ppolitica13 = Paragraph("Tarjetas loops, panel, estrobos, sensores fotoeléctricos, fuentes de poder, módulos de control. Monitores de flujo, resistencias de fin de línea.",styleN,bulletText="-")
        ppolitica14 = Paragraph("Atención a Emergencias en caso de falla total del panel principal y que la operación del 50% o mas del sistema este comprometida con un tiempo de respuesta en sitio de 4 hora.",styleN,bulletText="•")
        ppolitica16 = Paragraph("Los costos asociados de un dispositivo dañado será tomado en cuenta de la lista de precios que se proporciona en este documento en conjunto con el contrato, de esta manera cuando un dispositivo se dañen la facturación de la refacción sea en base a este precio.",styleN)



        table_dis = Table(listdisp)
        ts = TableStyle([("GRID",(0,0),(-1,-1),2,colors.black)])
        table_dis.setStyle(ts)

        td_mantenimientos = [["Mantenimiento",Paragraph("Acts. de mmnto por año"),
                            Paragraph("Acts. adicionales")
                            ,Paragraph("Tiempo de ejecucion")]]
        for mantenimiento in mantenimientos:
            if str(mantenimiento.titulonombre) != "Servicio de soporte técnico -Horas de servicios generales adicionales":
                if mantenimiento.periodisidadadicional is None:
                    data_mantenimientos = [Paragraph(str(mantenimiento.titulonombre)),mantenimiento.periodisidadactividades,0,mantenimiento.tiempoejecucion]
                else:
                    data_mantenimientos = [Paragraph(str(mantenimiento.titulonombre)),mantenimiento.periodisidadactividades,mantenimiento.periodisidadadicional,mantenimiento.tiempoejecucion]

                td_mantenimientos.append(data_mantenimientos)
        table_man = Table(td_mantenimientos,colWidths=[3*inch,1*inch,1*inch , 1*inch])
        table_man.setStyle(ts)

        td_total = [["Total de horas de servicio de soporte técnico incluidas en esta poliza","Horas",suma_horas]]
        table_tot = Table(td_total)
        ts_tot = TableStyle([("GRID",(0,0),(-1,-1),2,colors.black),
                             ("BACKGROUND",(0,0),(-1,-1),colors.yellow)])
        table_tot.setStyle(ts_tot)

        preciofinal = 0
        preciofinalincadicional = 0
        for mantenimiento in mantenimientos:
            preciofinal = preciofinal + mantenimiento.costomantenimientoregular
            preciofinalincadicional = preciofinalincadicional + mantenimiento.costomantenimientoregular + mantenimiento.costomantenimientoadicional
        preciofinal = float(round(preciofinal))
        preciofinal1 = num2words(preciofinal, to="currency", lang='es', currency='USD').upper()
        preciofinal = "${:,.2f}".format(preciofinal)
        preciofinalincadicional = float(round(preciofinalincadicional))
        preciofinalincadicional1 = num2words(preciofinalincadicional, to="currency", lang='es', currency='USD').upper()
        preciofinalincadicional = "${:,.2f}".format(preciofinalincadicional)
        
        ts_pre = TableStyle([("GRID",(0,0),(-1,-1),2,colors.black),
                             ("BACKGROUND",(0,0),(-1,0),colors.lightsteelblue)])
        td_precio = [["Descripcion","Cantidad","Unidad","Costo"]]
        td_precioadicional = [["Descripcion","Cantidad","Unidad","Costo"]]

        data_precio = [Paragraph("Cuota anual del contrato de  mantenimiento"), Paragraph("1",styleNC),Paragraph("Lot",styleNC),Paragraph("{}".format(preciofinal),styleNC)]
        data_precioadicional = [Paragraph("Cuota anual del contrato de  mantenimiento incluyendo periodicidad adicional"), Paragraph("1",styleNC),Paragraph("Lot",styleNC),Paragraph("{}".format(preciofinalincadicional),styleNC)]
        td_precio.append(data_precio)
        listmanteniminientos = []
        for mantenimiento in mantenimientos:
            if mantenimiento.costomantenimientoadicional != 0 and mantenimiento.costomantenimientoadicional != None:
                listmanteniminientos.append(mantenimiento.costomantenimientoadicional)
        if any(listmanteniminientos):
            td_precioadicional.append(data_precioadicional)
            table_preadicional = Table(td_precioadicional)
            table_preadicional.setStyle(ts_pre)
            ppreciotextoadicional = Paragraph(preciofinalincadicional1+" USD + IVA",styleNBC)
            p22adicional = Paragraph(actyear+"-"+sigyear+" Mantenimiento operativo regular y soporte técnico anual incluyendo periodicidad adicional",styleB)
            p23adicional = Paragraph("Total de Propuesta Económica de Mantenimiento Preventivo incluyendo periodicidad adicional",styleHBC)
            p24adicional = Paragraph("Poliza de mantenimiento "+actyear+"-"+sigyear+".............................{}".format(preciofinalincadicional),styleNY)
            p25adicional = Paragraph(preciofinalincadicional1+" USD + IVA",styleNY)

        table_pre = Table(td_precio)
        table_pre.setStyle(ts_pre)
        ppreciotexto = Paragraph(preciofinal1+" USD + IVA",styleNBC)
        p21 = Paragraph("3.0 Resumen de la propuesta económica",styleHB)
        p22 = Paragraph(actyear+"-"+sigyear+" Mantenimiento operativo regular y soporte técnico anual",styleB)


        p23 = Paragraph("Total de Propuesta Económica de Mantenimiento Preventivo",styleHBC)
        p24 = Paragraph("Poliza de mantenimiento "+actyear+"-"+sigyear+".............................{}".format(preciofinal),styleNY)
        p25 = Paragraph(preciofinal1+" USD + IVA",styleNY)

        ptitulotermino = Paragraph("4.0 Términos y condiciones",styleHB)
        pterminos1 = Paragraph("Los precios cotizados se expresan en dólares americanos.",styleN,bulletText="-")
        pterminos2 = Paragraph("El IVA del 16% no está incluido.",styleN,bulletText="-")
        pterminos3 = Paragraph("El tipo de cambio será el de Banco BBVA a la venta en la ventanilla vigente el día de la operación de pago efectivo. LOS PAGOS NO SE ACEPTAN UTILIZANDO EL TIPO DE CAMBIO DEL DIARIO OFICIAL DE LA FEDERACIÓN.",styleN,bulletText="-")
        pterminos4 = Paragraph("Válido de la oferta: 30 días naturales, posteriormente los precios están sujetos a cambios sin previo aviso.",styleN,bulletText="-")
        pterminos5 = Paragraph("El proceso comienza confirmando su pago total o anticipo según sea el caso y su colocación del pedido de compra.",styleN,bulletText="-")
        #pterminos6 = Paragraph("Para proceder con el mantenimiento correctivo, es necesario cubrir la póliza anual al 100% en el primer día de atención.",styleN,bulletText="-")
        pterminos7 = Paragraph("Para proceder con el mantenimiento preventivo, es necesario cubrir la anualidad de la póliza al 100% el primer día de la primera visita programada.",styleN,bulletText="-")
        pterminos8 = Paragraph("Los precios indicados son ofrecidos por el Total de la Propuesta aquí citado, cualquier cambio de condiciones o equipo seleccionado debe ser citado de nuevo.",styleN,bulletText="-")
        pterminos9 = Paragraph("Tiempo de entrega: se coordinar con el área de operaciones para asignar la fecha y hora de ejecución, esta fecha no debe de ser mayor a 7 días calendarios después de la recepción de pago por la póliza.",styleN,bulletText="-")

        info = InformacionPersonal.objects.get(user=usuario)
        nombrecontitulo = str(info.titulo)+"."+" "+str(info.nombre)+" "+str(info.apellido)
        puesto = str(info.puesto)
        pfin = Paragraph("Fin del documento",styleNC)
        pregards = Paragraph("Regards",styleNC)
        pdanieljara = Paragraph(nombrecontitulo,styleNC)
        pdirector = Paragraph(puesto,styleNC)

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
        Story.append(pblank)
        Story.append(p1extra)
        Story.append(PageBreak())

        #Tercera pagina
        Story.append(p15)
        Story.append(pblank)
        Story.append(p16)
        Story.append(pblank)
        Story.append(p2extra)
        Story.append(pblank)
        Story.append(p17)
        Story.append(pblank)
        Story.append(p3extra)
        Story.append(pblank)
        Story.append(p4extra)
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
        Story.append(p5extra)
        Story.append(pblank)
        Story.append(palcances1)
        Story.append(palcances2)
        Story.append(palcances3)
        Story.append(palcances4)
        Story.append(palcances5)
        Story.append(palcances6)
        Story.append(palcances7)
        Story.append(palcances8)
        Story.append(palcances9)
        Story.append(palcances10)
        Story.append(pblank)
        Story.append(p6extra)
        Story.append(pblank)
        Story.append(palcances12)
        Story.append(palcances13)
        Story.append(palcances14)
        Story.append(palcances15)
        Story.append(palcances16)
        Story.append(pblank)

        Story.append(PageBreak())


        Story.append(ppolitica)
        Story.append(ppoliticaextra1)
        Story.append(pblank)
        Story.append(ppolitica1)
        Story.append(ppolitica16)
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
        # Story.append(ppolitica13)
        Story.append(ppolitica14)


        Story.append(PageBreak())

        #Sexta pagina
        Story.append(p21)
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
        if any(listmanteniminientos):
            Story.append(pblank)
            Story.append(pblank)
            Story.append(p22adicional)
            Story.append(pblank)
            Story.append(table_preadicional)
            Story.append(ppreciotextoadicional)
            Story.append(pblank)
            Story.append(pblank)
            Story.append(p23adicional) 
            Story.append(p24adicional)
            Story.append(p25adicional)
            Story.append(pblank)
            Story.append(pblank)

        Story.append(PageBreak())

        #Septima pagina
        Story.append(ptitulotermino)
        Story.append(pterminos1)
        Story.append(pterminos2)
        Story.append(pterminos3)
        Story.append(pterminos4)
        Story.append(pterminos5)
        #Story.append(pterminos6)
        Story.append(pterminos7)
        Story.append(pterminos8)
        Story.append(pterminos9)
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
