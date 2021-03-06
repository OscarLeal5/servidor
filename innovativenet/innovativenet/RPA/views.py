from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak, Table, TableStyle, Indenter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.rl_config import defaultPageSize
from django.shortcuts import render, redirect
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from django.http import FileResponse
from django.urls import reverse
from reportlab.lib import colors
from datetime import datetime
import locale
from .models import *
from datetime import date
import io
import os
from pathlib import Path
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


# ------ VIEWS COTIZACION DETECCION FUEGO------ #

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
        ctx['servicios'] = ctx['servicios'].exclude(titulonombre=Nombre_servicio.objects.get(pk=14))
        ctx['servicios'] = ctx['servicios'].exclude(titulonombre=Nombre_servicio.objects.get(pk=15))

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

# ------ VIEWS COTIZACION CCTV------ #

class Agregar_Cotizacion_CCTV(LoginRequiredMixin, CreateView):
    model = Cotizacion_CCTV
    #cambios area de trabajo
    fields = ['titulo', 'lugar_de_mantenimiento','area_de_mantenimiento', 'descripcion_cotizacion','periodoregular','preguntaperiodoadicional','periodoadicional']
    #cambios    
    template_name = 'cotizacion_cctv/agregar_cotizacion_cctv.html'

    def form_valid(self, form):
        form.instance.cliente = Cliente.objects.get(pk=self.kwargs['cliente'])
        return super(Agregar_Cotizacion_CCTV, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('detalle_cotizacion_cctv', kwargs={'cliente':self.object.cliente.pk, 'pk':self.object.pk})

class Detalle_Cotizacion_CCTV(LoginRequiredMixin, DetailView):
    model = Cotizacion_CCTV
    object = "cotizacion_cctv"
    template_name = "cotizacion_cctv/detalle_cotizacion_cctv.html"
    def get_context_data(self, **kwargs):
        ctx = super(Detalle_Cotizacion_CCTV, self).get_context_data(**kwargs)
        # del diccionario de Key Word ARGumentS obtiene el valor de object
        cat = kwargs.get("object")
        ctx['servicios'] = Mantenimiento_CCTV.objects.filter(cotizacion = cat)
        ctx['servicios'] = ctx['servicios'].exclude(titulonombre=Nombre_servicio_CCTV.objects.get(pk=5))
        ctx['servicios'] = ctx['servicios'].exclude(titulonombre=Nombre_servicio_CCTV.objects.get(pk=16))
        ctx['servicios'] = ctx['servicios'].exclude(titulonombre=Nombre_servicio_CCTV.objects.get(pk=6))
        ctx['servicios'] = ctx['servicios'].exclude(titulonombre=Nombre_servicio_CCTV.objects.get(pk=20))
        ctx['servicios'] = ctx['servicios'].exclude(titulonombre=Nombre_servicio_CCTV.objects.get(pk=19))
        ctx['servicios'] = ctx['servicios'].exclude(titulonombre=Nombre_servicio_CCTV.objects.get(pk=7))
        ctx['servicios'] = ctx['servicios'].exclude(titulonombre=Nombre_servicio_CCTV.objects.get(pk=21))
        ctx['serviciosplus'] = Mantenimiento_CCTV.objects.filter(cotizacion = cat,titulonombre=Nombre_servicio_CCTV.objects.get(pk=6))

        #ctx['']
        return ctx
        
class Modificar_Cotizacion_CCTV(LoginRequiredMixin, UpdateView):
    model = Cotizacion_CCTV
    object = "cotizacion"
    fields = ['titulo', 'lugar_de_mantenimiento','area_de_mantenimiento' ,'descripcion_cotizacion']
    template_name = 'cotizacion_cctv/modificar_cotizacion_cctv.html'
    def get_success_url(self):
        return reverse('mostrar_cliente', kwargs={'pk':self.object.cliente.id})

class Eliminar_Cotizacion_CCTV(LoginRequiredMixin, DeleteView):
    model = Cotizacion_CCTV
    context_object_name = "cotizacion_cctv"
    template_name = "cotizacion_cctv/eliminar_cotizacion_cctv.html"

    def get_success_url(self):
        return reverse('mostrar_cliente', kwargs={'pk':self.object.cliente.id})

# ------ VIEWS COTIZACION CA------ #

class Agregar_Cotizacion_CA(LoginRequiredMixin, CreateView):
    model = Cotizacion_CA
    fields = ['titulo', 'lugar_de_mantenimiento', 'descripcion_cotizacion','periodoregular','preguntaperiodoadicional','periodoadicional']
    template_name = 'cotizacion_ca/agregar_cotizacion_ca.html'

    def form_valid(self, form):
        form.instance.cliente = Cliente.objects.get(pk=self.kwargs['cliente'])
        return super(Agregar_Cotizacion_CA, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('detalle_cotizacion_ca', kwargs={'cliente':self.object.cliente.pk, 'pk':self.object.pk})

class Detalle_Cotizacion_CA(LoginRequiredMixin, DetailView):
    model = Cotizacion_CA
    object = "cotizacion_ca"
    template_name = "cotizacion_ca/detalle_cotizacion_ca.html"
    def get_context_data(self, **kwargs):
        ctx = super(Detalle_Cotizacion_CA, self).get_context_data(**kwargs)
        # del diccionario de Key Word ARGumentS obtiene el valor de object
        cat = kwargs.get("object")
        ctx['servicios'] = Mantenimiento_CA.objects.filter(cotizacion = cat)
        ctx['servicios'] = ctx['servicios'].exclude(titulonombre=Nombre_servicio_CA.objects.get(pk=1))
        ctx['servicios'] = ctx['servicios'].exclude(titulonombre=Nombre_servicio_CA.objects.get(pk=2))
        ctx['servicios'] = ctx['servicios'].exclude(titulonombre=Nombre_servicio_CA.objects.get(pk=3))

        ctx['serviciosplus'] = Mantenimiento_CA.objects.filter(cotizacion = cat,titulonombre=Nombre_servicio_CA.objects.get(pk=2))

        #ctx['']
        return ctx
        
class Modificar_Cotizacion_CA(LoginRequiredMixin, UpdateView):
    model = Cotizacion_CA
    object = "cotizacion_ca"
    fields = ['titulo', 'lugar_de_mantenimiento', 'descripcion_cotizacion']
    template_name = 'cotizacion_ca/modificar_cotizacion_ca.html'
    def get_success_url(self):
        return reverse('mostrar_cliente', kwargs={'pk':self.object.cliente.id})

class Eliminar_Cotizacion_CA(LoginRequiredMixin, DeleteView):
    model = Cotizacion_CA
    context_object_name = "cotizacion_ca"
    template_name = "cotizacion_ca/eliminar_cotizacion_ca.html"

    def get_success_url(self):
        return reverse('mostrar_cliente', kwargs={'pk':self.object.cliente.id})

# ------ VIEWS MANTENIMIENTOS DETECCION FUEGO ------ #

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

# ------ VIEWS MANTENIMIENTOS CCTV ------ #

class Agregar_Mantenimiento_CCTV(LoginRequiredMixin, CreateView):
    # Manda a llamar el Modelo Mantenimiento
    model = Mantenimiento_CCTV
    # Hace la eleccion de que inputs del Modelo tomar en cuenta
    fields = ['titulonombre', 'periodisidadactividades', 'periodisidadadicional',
                'cantidaddedispositivos', 'cantidaddispositivosextras',
                ]
    # Busca un html en especifico
    template_name = 'mantenimientos_cctv/agregar_servicio.html'

    # Cuando se confirma el mantenimiento
    def form_valid(self, form):
        # se agrega el usuario que se esta usando en la instancia de usuario
        form.instance.cliente = Cliente.objects.get(pk=self.kwargs['cliente'])
        form.instance.cotizacion = Cotizacion_CCTV.objects.get(pk=self.kwargs['pk'])
        return super(Agregar_Mantenimiento_CCTV, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('detalle_cotizacion_cctv', kwargs={'pk':self.object.cotizacion.id,'cliente':self.object.cotizacion.cliente.id})

class MttoUpdate_CCTV(LoginRequiredMixin, UpdateView):
    model = Mantenimiento_CCTV
    context_object_name = 'servicio'
    fields = ['periodisidadactividades', 'periodisidadadicional','cantidaddedispositivos', 'cantidaddispositivosextras','tiempoejecucion']
    template_name = 'mantenimientos_cctv/modificar_servicio.html'

    def get_success_url(self):
        return reverse('detalle_cotizacion_cctv', kwargs={'pk':self.object.cotizacion.id,'cliente':self.object.cotizacion.cliente.id})

class EliminarMantenimiento_CCTV(LoginRequiredMixin, DeleteView):
    model = Mantenimiento_CCTV
    context_object_name = 'servicio'
    template_name = 'mantenimientos_cctv/eliminar_servicio.html'
    
    def get_success_url(self):
        return reverse('detalle_cotizacion_cctv', kwargs={'cliente':self.object.cotizacion.cliente.id,'pk':self.object.cotizacion.id})

class Detalle_Servicio_CCTV(LoginRequiredMixin, DetailView):
    model = Mantenimiento_CCTV
    context_object_name = 'servicio'
    template_name = 'mantenimientos_cctv/detalle_servicio.html'

# ------ VIEWS MANTENIMIENTOS CA ------ #

class Agregar_Mantenimiento_CA(LoginRequiredMixin, CreateView):
    # Manda a llamar el Modelo Mantenimiento
    model = Mantenimiento_CA
    # Hace la eleccion de que inputs del Modelo tomar en cuenta
    fields = ['titulonombre', 'periodisidadactividades', 'periodisidadadicional',
                'cantidaddedispositivos', 'cantidaddispositivosextras',
                ]
    # Busca un html en especifico
    template_name = 'mantenimientos_ca/agregar_servicio.html'

    # Cuando se confirma el mantenimiento
    def form_valid(self, form):
        # se agrega el usuario que se esta usando en la instancia de usuario
        form.instance.cliente = Cliente.objects.get(pk=self.kwargs['cliente'])
        form.instance.cotizacion = Cotizacion_CA.objects.get(pk=self.kwargs['pk'])
        return super(Agregar_Mantenimiento_CA, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('detalle_cotizacion_ca', kwargs={'pk':self.object.cotizacion.id,'cliente':self.object.cotizacion.cliente.id})

class MttoUpdate_CA(LoginRequiredMixin, UpdateView):
    model = Mantenimiento_CA
    context_object_name = 'servicio'
    fields = ['periodisidadactividades', 'periodisidadadicional','cantidaddedispositivos', 'cantidaddispositivosextras','tiempoejecucion']
    template_name = 'mantenimientos_ca/modificar_servicio.html'

    def get_success_url(self):
        return reverse('detalle_cotizacion_ca', kwargs={'pk':self.object.cotizacion.id,'cliente':self.object.cotizacion.cliente.id})

class EliminarMantenimiento_CA(LoginRequiredMixin, DeleteView):
    model = Mantenimiento_CA
    context_object_name = 'servicio'
    template_name = 'mantenimientos_ca/eliminar_servicio.html'
    
    def get_success_url(self):
        return reverse('detalle_cotizacion_ca', kwargs={'cliente':self.object.cotizacion.cliente.id,'pk':self.object.cotizacion.id})

class Detalle_Servicio_CA(LoginRequiredMixin, DetailView):
    model = Mantenimiento_CA
    context_object_name = 'servicio'
    template_name = 'mantenimientos_ca/detalle_servicio.html'

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
        ctx['cotizaciones_cctv'] = Cotizacion_CCTV.objects.filter(cliente = cat)
        ctx['cotizaciones_ca'] = Cotizacion_CA.objects.filter(cliente = cat)
        return ctx






# --------- DESCARGA PDF ----------------------------

def cotizacion_pdf(request, cliente_id,cotizacion_id,usuario):

    cliente = Cliente.objects.get(pk=cliente_id)
    cotizacion = Cotizacion.objects.get(pk=cotizacion_id,cliente=cliente_id)
    # mantenimientos = Cliente.mantenimiento.through.objects.
    buf = io.BytesIO()

    nombre=cliente.nombre
    lugar_de_mantenimiento = cotizacion.lugar_de_mantenimiento
    descripcion_cotizacion = cotizacion.descripcion_cotizacion

    locale.setlocale(locale.LC_TIME, 'es-ES')
    dateTimeObj = datetime.now()
    dateStr = dateTimeObj.strftime("%d de %B del %Y ")

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
                              leading=12,
                              ))
    styles.add(ParagraphStyle(name='Normal_J',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_JUSTIFY,
                              fontSize=10,
                              textColor=colors.black,
                              leading=15,))
    styles.add(ParagraphStyle(name='Normal_C',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.black,
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Right',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_RIGHT,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              leading=12,))

    styles.add(ParagraphStyle(name='Heading1_B',
                              parent=styles['Heading1'],
                              wordWrap='LTR',
                              alignment=TA_LEFT,
                              fontSize=12,
                              textColor=colors.HexColor("#3498DB"),
                              leading=12,))
    styles.add(ParagraphStyle(name='Heading1_BC',
                              parent=styles['Heading1'],
                              wordWrap='LTR',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.HexColor("#3498DB"),
                              leading=12,))

    styles.add(ParagraphStyle(name='Normal_CB',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_B',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_LEFT,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Red',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_LEFT,
                              fontSize=12,
                              textColor=colors.red,
                              fontName="Helvetica-bold",
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Ye',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              backColor = colors.yellow,
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Center',
                            parent=styles['Normal'],
                            wordWrap='CJK',
                            alignment=TA_CENTER,
                            fontSize=12,
                            textColor=colors.black,
                            fontName="Helvetica-bold",
                            leading=12,))



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
        p6 = Paragraph("Estimados se??ores, ", styleN)
        p7 = Paragraph("En relaci??n con su solicitud nos complace presentar la propuesta de mantenimiento del sistema de detecci??n de incendios, en este documento se presenta la propuesta econ??mica basados en las caracter??sticas de su edificio y sus equipos actuales en la compa????a "+nombre+" ubicada en la ciudad de "+lugar_de_mantenimiento, styleN)
        pblank = Paragraph("""<para> <br/> </para>""")
        p8 = Paragraph("??ndice de propuesta:, ", styleN)
        p9 = Paragraph("1.0 Fondo", styleN)
        p10 = Paragraph("2.0 Alcance de la descripci??n del trabajo", styleN)
        p11 = Paragraph("3.0 Resumen de propuestas econ??micas", styleN)
        p12 = Paragraph("4.0 T??rminos y condiciones", styleN)
        p13 = Paragraph("1.0 Fondo", styleHB)
        p14 = Paragraph("A continuaci??n en la tabla de abajo se muestra una visi??n general de los equipos , as?? como las visitas de mantenimiento anual consideradas en un a??o calendario, la columna cantidad indica el numero de dispositivos considerados a mantener en esta oferta econ??mica de cada tipo de manera regular en base ya sea a nuestras recomendaci??n o a las pol??ticas de seguridad establecidas por el cliente.",styleN)
        p1extra = Paragraph("Regularmente las visitas adicionales por a??o son aquellas visitas que proponemos realizar adicional a las visitas regulares  ya sea porque est??n sujetas a condiciones de clima, polvos, suciedad o qu??micos fuera de lo normal, pueden dispositivos en ??reas en construcciones remodelaciones o presencia de qu??micos, si la columna esta en ???0??? esto significa que no se esta considerando ninguna zona como anteriormente se explica.",styleN)
        p15 = Paragraph("1.1 Politica de mantenimiento preventivo",styleHB)
        p16 = Paragraph("Para proceder y aplicar un mantenimiento preventivo se entiende que el sistema de detecci??n de incendios debe estar en operaci??n al 100% sin ninguna falla o problema, si este no cumple deber?? de realizarse primero un mantenimiento correctivo bajo presupuesto adicional que no forma parte de este presupuesto.",styleN)
        p2extra = Paragraph("El mantenimiento preventivo considera un compromiso de la empresa para la ejecuci??n de una serie de acciones a el panel y dispositivos de manera calendarizada bajo una fecha establecida con la finalidad de mantener la operaci??n del sistema al 100% funcional desde el inicio de la fecha de contrato hasta 365 d??as despu??s de la firma del mismo.",styleN)
        listdisp = [["Dispositivo","Cantidad",Paragraph("Visitas por a??o"),Paragraph("Visitas adicionales por a??o"),Paragraph("Dispositivos en periodicidad adcional")]]
        mantenimientos = Mantenimiento.objects.filter(cliente = cliente_id,cotizacion=cotizacion_id)
        for mantenimiento in mantenimientos:
            if mantenimiento.periodisidadadicional is not None or mantenimiento.periodisidadadicional != 0:
                if mantenimiento.dispositivo is not None:
                    if mantenimiento.periodisidadadicional is None:
                        info_disp = [Paragraph(mantenimiento.dispositivo),mantenimiento.cantidaddedispositivos,mantenimiento.periodisidadactividades,0,0]
                    else:    
                        info_disp = [Paragraph(mantenimiento.dispositivo),mantenimiento.cantidaddedispositivos,mantenimiento.periodisidadactividades,mantenimiento.periodisidadadicional,mantenimiento.cantidaddispositivosextras]
                    listdisp.append(info_disp)
            else:
                if mantenimiento.dispositivo is not None:
                    info_disp = [Paragraph(mantenimiento.dispositivo),mantenimiento.cantidaddedispositivos]
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
        p17 = Paragraph("Se considera dentro de los dispositivos a mantener el equipo que actualmente cuentan consider??ndose "+str(listadispositivos),styleN)
        p3extra = Paragraph("Total de dispositivos: "+str(totaldisp.cantidaddedispositivos), styleN)
        p4extra = Paragraph("La maquinaria de elevaci??n es necesaria utilizarse en dispositivos mas de 15 pies de altura, este tipo de equipo tienen un costo asociado por su traslado al sitio y recolecci??n, su uso por d??a y es necesario recargarse bajo una toma el??ctrica, esta maquinaria de elevaci??n no esta considerada en su costo, por lo que queda por responsabilidad del cliente solicitar una de ser necesaria para este trabajo de mantenimiento en las visitas que sean necesaria de una manera programada, as?? como las facilidades el??ctricas para la recarga del equipo.",styleN)
        p18 = Paragraph("Periodo de cobertura "+actyear+"-"+sigyear,styleB)
        p19 = Paragraph("En la siguiente tabla se muestran las actividades que se consideran.",styleB)
        p20 = Paragraph("2.0 Alcance de la descripci??n del trabajo",styleHB)
        p5extra = Paragraph("Que se Incluye en esta p??liza de mantenimiento del sistema de detecci??n de fuego?: ",styleB)
        if cotizacion.periodoregular == 1:
            palcances1= Paragraph(str(cotizacion.periodoregular)+" visita de actividades de mantenimiento al a??o.",styleN,bulletText="???")
        else:
            palcances1= Paragraph(str(cotizacion.periodoregular)+" visitas de actividades de mantenimiento al a??o.",styleN,bulletText="???")
        ppolitica16 = Paragraph("Disponibilidad de portal WEB personalizado para el seguimiento por personal asignado del cliente con todo el Equipo t??cnico de la empresa para visualizaci??n de las actividades de mantenimiento y reportes.",styleN,bulletText="???")
        palcances2 = Paragraph("Poner el sistema en modo de prueba.",styleN,bulletText="???")
        palcances3 = Paragraph("De manera calendarizada cada Visita  se ejecutara la limpieza de los sensores y m??dulos f??sicamente. Los dispositivos para limpiar dando mayor jerarqu??a  son los que determine el reporte de mantenimiento y sensibilidad que indique un nivel de suciedad mayor al 35% despu??s se procede con el resto.",styleN,bulletText="???")
        palcances4 = Paragraph("Limpieza de panel de alarmas ( pantalla LCD, conectores, terminales de cableado, limpieza, sellos silic??n, revisi??n de conectividad a panel remoto y actividad en el Lazo SLC de dispositivos).",styleN,bulletText="???")
        palcances5 = Paragraph("Reporte de sensibilidad el cual nos indica que sensor est?? sucio de sus elementos internos para proceder a limpiarlos.",styleN,bulletText="???")
        palcances6 = Paragraph("Limpieza de estrobos-cornetas y palancas.",styleN,bulletText="???")
        palcances7 = Paragraph("Prueba de verificaci??n de leds del panel , iluminar todos los leds.",styleN,bulletText="???")
        palcances8 = Paragraph("Prueba de verificaci??n de energ??a primaria, remover energ??a de AC, verificar que el panel funcione con bater??as, verificar que el panel entre en modo de problema, restablecer energ??a y dejar todo en orden en modo normal.",styleN,bulletText="???")

        palcances9 = Paragraph("Prueba de se??ales de problema en panel  funcionen apropiadamente",styleN,bulletText="???")
        palcances10 = Paragraph("Verificaci??n bimestral que la pantalla LCD del panel marque la hora apropiada.",styleN,bulletText="???")
        p6extra = Paragraph("""<u>??Que no se incluye?:</u>""",styleB)

        
        palcances12= Paragraph("Equipos y Refacciones.",styleN,bulletText="1.")
        palcances13= Paragraph("Materiales como cables o tuber??as.",styleN,bulletText="2.")
        palcances14= Paragraph("Maquinaria de elevaci??n.",styleN,bulletText="3.")
        palcances15= Paragraph("Trabajos en d??as Festivos",styleN,bulletText="4.")
        palcances16= Paragraph("Trabajos fuera del horario establecido.",styleN,bulletText="5.")
        suma_horas = 0
        for mantenimiento in mantenimientos:
            if str(mantenimiento.titulonombre) == "Servicio de soporte t??cnico -Horas de servicios generales adicionales":
                suma_horas = mantenimiento.tiempoejecucion
        suma_horas_palabra = num2words(suma_horas,lang='es')
        

        ppolitica = Paragraph("2.1 Pol??tica de apoyo t??cnico y diagn??stico",styleHB)
        ppoliticaextra1=Paragraph("""<u>??Que se Incluye en las horas de Servicios de soporte T??cnico, pruebas y servicios de reparaci??n consideradas en esta propuesta?:</u>""",styleB)
        ppolitica1 = Paragraph("Servicio de soporte t??cnico para diagnostico o correcci??n por "+str(suma_horas)+" horas o 12 meses, lo que suceda primero.  ",styleN,bulletText="???")
        ppolitica2 = Paragraph("D??as regular para Soporte t??cnico de Lunes a s??bado (horarios de 8.00am ??? 6:00pm)",styleN,bulletText="???")
        ppolitica3 = Paragraph("Atenci??n t??cnica y reparaci??n de fallas en los paneles o en los dispositivos en su red.",styleN,bulletText="???")
        ppolitica4 = Paragraph("Tiempo de respuesta de servicios normal: siguiente d??a h??bil.",styleN,bulletText="???")
        ppolitica5 = Paragraph("Prueba semestral de palancas manuales, inspecci??n visual, activar el mecanismo y confirmar respuesta en la zona apropiada.",styleN,bulletText="???")
        ppolitica6 = Paragraph("Prueba semestral de detectores de calor, inspecci??n visual, conducir una funci??n de prueba para verificar la respuesta en la zona apropiada.",styleN,bulletText="???")
        ppolitica7 = Paragraph("Prueba anual de detectores de humo, conducir una funci??n de prueba para verificar la respuesta en la zona apropiada.",styleN,bulletText="???")
        ppolitica8 = Paragraph("Prueba semestral de todos los dispositivos de iniciaci??n de alarmas, activar los dispositivos y verificar que los circuitos de aplicaci??n de notificaci??n apropiados est??n funcionando correctamente (NAC) as?? como informaci??n de zona y mensajes correspondientes, abrir el cableado de campo de los dispositivos de iniciaci??n y verificar que el mensaje de problema se indique en el panel.",styleN,bulletText="???")
        ppolitica9 = Paragraph("Prueba anual de Notificaci??n en cornetas-estrobos, colocar el panel en alarma, drill o modo de prueba y verificar que todos los notificadores est??n trabajando apropiadamente.",styleN,bulletText="???")
        ppolitica10 = Paragraph("Prueba de energ??a secundaria en los paneles principales y remotos, remover energ??a primaria de AC, medir corrientes en modo ???stand by??? y  alarmado y comparar con c??lculo de bater??as para verificar una capacidad de bater??a adecuada, probar a plena carga por 5 minutos, medir voltajes de bater??as a plena carga, restablecer energ??a primaria de AC al final de la prueba, restablecer y cerrar panel al final de la prueba.",styleN,bulletText="???")
        ppolitica11 = Paragraph("Mano de obra por remplazo de cualquier refacci??n como m??dulos, sensores, tarjetas, paneles, fuentes de poder, cables",styleN,bulletText="???")
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


        ppolitica12 = Paragraph("Tiempo de  Programaci??n y configuraci??n de Paneles  sobre los equipos dentro de la p??liza de mantenimiento.",styleN,bulletText="???")
        #ppolitica13 = Paragraph("Tarjetas loops, panel, estrobos, sensores fotoel??ctricos, fuentes de poder, m??dulos de control. Monitores de flujo, resistencias de fin de l??nea.",styleN,bulletText="-")
        ppolitica14 = Paragraph("Atenci??n a Emergencias en caso de falla total del panel principal y que la operaci??n del 50% o mas del sistema este comprometida con un tiempo de respuesta en sitio de 4 hora.",styleN,bulletText="???")
        ppolitica16 = Paragraph("Los costos asociados de un dispositivo da??ado ser?? tomado en cuenta de la lista de precios que se proporciona en este documento en conjunto con el contrato, de esta manera cuando un dispositivo se da??en la facturaci??n de la refacci??n sea en base a este precio.",styleN)



        table_dis = Table(listdisp, colWidths=[3*inch,1*inch,1*inch , 1*inch])
        ts = TableStyle([("GRID",(0,0),(-1,-1),2,colors.black)])
        table_dis.setStyle(ts)

        td_mantenimientos = [["Mantenimiento",Paragraph("Acts. de mmnto por a??o"),
                            Paragraph("Acts. adicionales")
                            ,Paragraph("Tiempo de ejecucion")]]
        for mantenimiento in mantenimientos:
            if str(mantenimiento.titulonombre) != "Servicio de soporte t??cnico -Horas de servicios generales adicionales":
                if mantenimiento.periodisidadadicional is None:
                    data_mantenimientos = [Paragraph(str(mantenimiento.titulonombre)),mantenimiento.periodisidadactividades,0,mantenimiento.tiempoejecucion]
                else:
                    data_mantenimientos = [Paragraph(str(mantenimiento.titulonombre)),mantenimiento.periodisidadactividades,mantenimiento.periodisidadadicional,mantenimiento.tiempoejecucion]

                td_mantenimientos.append(data_mantenimientos)
        table_man = Table(td_mantenimientos,colWidths=[3*inch,1*inch,1*inch , 1*inch])
        table_man.setStyle(ts)

        td_total = [["Total de horas de servicio de soporte t??cnico incluidas en esta poliza","Horas",suma_horas]]
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
            p22adicional = Paragraph(actyear+"-"+sigyear+" Mantenimiento operativo regular y soporte t??cnico anual incluyendo periodicidad adicional",styleB)
            p23adicional = Paragraph("Total de Propuesta Econ??mica de Mantenimiento Preventivo incluyendo periodicidad adicional",styleHBC)
            p24adicional = Paragraph("Poliza de mantenimiento "+actyear+"-"+sigyear+".............................{}".format(preciofinalincadicional),styleNY)
            p25adicional = Paragraph(preciofinalincadicional1+" USD + IVA",styleNY)

        table_pre = Table(td_precio)
        table_pre.setStyle(ts_pre)
        ppreciotexto = Paragraph(preciofinal1+" USD + IVA",styleNBC)
        p21 = Paragraph("3.0 Resumen de la propuesta econ??mica",styleHB)
        p22 = Paragraph(actyear+"-"+sigyear+" Mantenimiento operativo regular y soporte t??cnico anual",styleB)


        p23 = Paragraph("Total de Propuesta Econ??mica de Mantenimiento Preventivo",styleHBC)
        p24 = Paragraph("Poliza de mantenimiento "+actyear+"-"+sigyear+".............................{}".format(preciofinal),styleNY)
        p25 = Paragraph(preciofinal1+" USD + IVA",styleNY)

        ptitulotermino = Paragraph("4.0 T??rminos y condiciones",styleHB)
        pterminos1 = Paragraph("Los precios cotizados se expresan en d??lares americanos.",styleN,bulletText="-")
        pterminos2 = Paragraph("El IVA del 16% no est?? incluido.",styleN,bulletText="-")
        pterminos3 = Paragraph("El tipo de cambio ser?? el de Banco BBVA a la venta en la ventanilla vigente el d??a de la operaci??n de pago efectivo. LOS PAGOS NO SE ACEPTAN UTILIZANDO EL TIPO DE CAMBIO DEL DIARIO OFICIAL DE LA FEDERACI??N.",styleN,bulletText="-")
        pterminos4 = Paragraph("V??lido de la oferta: 30 d??as naturales, posteriormente los precios est??n sujetos a cambios sin previo aviso.",styleN,bulletText="-")
        pterminos5 = Paragraph("El proceso comienza confirmando su pago total o anticipo seg??n sea el caso y su colocaci??n del pedido de compra.",styleN,bulletText="-")
        #pterminos6 = Paragraph("Para proceder con el mantenimiento correctivo, es necesario cubrir la p??liza anual al 100% en el primer d??a de atenci??n.",styleN,bulletText="-")
        pterminos7 = Paragraph("Para proceder con el mantenimiento preventivo, es necesario cubrir la anualidad de la p??liza al 100% el primer d??a de la primera visita programada.",styleN,bulletText="-")
        pterminos8 = Paragraph("Los precios indicados son ofrecidos por el Total de la Propuesta aqu?? citado, cualquier cambio de condiciones o equipo seleccionado debe ser citado de nuevo.",styleN,bulletText="-")
        pterminos9 = Paragraph("Tiempo de entrega: se coordinar con el ??rea de operaciones para asignar la fecha y hora de ejecuci??n, esta fecha no debe de ser mayor a 7 d??as calendarios despu??s de la recepci??n de pago por la p??liza.",styleN,bulletText="-")

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
    return FileResponse(buf, as_attachment=True,  filename='cotizacion_fuego_{}.pdf'.format(nombre))

def cotizacion_pdf_cctv(request, cliente_id,cotizacion_id,usuario):

    cliente = Cliente.objects.get(pk=cliente_id)
    cotizacion = Cotizacion_CCTV.objects.get(pk=cotizacion_id,cliente=cliente_id)
    # mantenimientos = Cliente.mantenimiento.through.objects.
    buf = io.BytesIO()

    nombre=cliente.nombre
    lugar_de_mantenimiento = cotizacion.lugar_de_mantenimiento
    # cambios area de mantenimiento
    area_de_mantenimiento = cotizacion.area_de_mantenimiento
    # cambios 
    descripcion_cotizacion = cotizacion.descripcion_cotizacion
    
    locale.setlocale(locale.LC_TIME, 'es-ES')
    dateTimeObj = datetime.now()
    dateStr = dateTimeObj.strftime("%d de %B del %Y ")

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
                              leading=12,
                              ))
    styles.add(ParagraphStyle(name='Normal_J',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_JUSTIFY,
                              fontSize=10,
                              textColor=colors.black,
                              leading=15,))
    styles.add(ParagraphStyle(name='Normal_C',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.black,
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Right',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_RIGHT,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              leading=12,))

    styles.add(ParagraphStyle(name='Heading1_B',
                              parent=styles['Heading1'],
                              wordWrap='LTR',
                              alignment=TA_LEFT,
                              fontSize=12,
                              textColor=colors.HexColor("#3498DB"),
                              leading=12,))
    styles.add(ParagraphStyle(name='Heading1_BC',
                              parent=styles['Heading1'],
                              wordWrap='LTR',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.HexColor("#3498DB"),
                              leading=12,))

    styles.add(ParagraphStyle(name='Normal_CB',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_B',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_LEFT,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Red',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_LEFT,
                              fontSize=12,
                              textColor=colors.red,
                              fontName="Helvetica-bold",
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Ye',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              backColor = colors.yellow,
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Center',
                            parent=styles['Normal'],
                            wordWrap='CJK',
                            alignment=TA_CENTER,
                            fontSize=12,
                            textColor=colors.black,
                            fontName="Helvetica-bold",
                            leading=12,))



    def myFirstPage(canvas, doc):
        BASE_DIR = Path(__file__).resolve().parent.parent
        canvas.saveState()
        canvas.setFont('Times-Bold', 16)
        canvas.setFont('Times-Roman', 14)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','logo.png'), 0.8 * inch, 660, width=160, height=80)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','footer.png'), inch, 1, width=460, height=80)
        canvas.restoreState()

    def myLaterPages(canvas, doc):
        BASE_DIR = Path(__file__).resolve().parent.parent
        canvas.saveState()
        canvas.setFont('Times-Roman', 9)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','logo.png'), 0.8 * inch, 660, width=160, height=80)
        canvas.drawImage(os.path.join(BASE_DIR,'RPA','img_pdf','footer.png'), inch, 1, width=460, height=80)
        canvas.restoreState()

    def go():
        cliente = Cliente.objects.get(pk=cliente_id)
        mantenimientos = Mantenimiento_CCTV.objects.filter(cliente = cliente_id,cotizacion=cotizacion_id)
        for mantenimiento in mantenimientos:
            listdisp = []
            listdisp.append(mantenimiento.dispositivo)
        cliente = Cliente.objects.get(pk=cliente_id)
        cotizacion = Cotizacion_CCTV.objects.get(pk=cotizacion_id,cliente=cliente_id)
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
        p6 = Paragraph("Estimados se??ores, ", styleN)
        #cambios para area de mantenimiento
        p7 = Paragraph("En relaci??n a su solicitud presentamos los costos asociados del servicio de mantenimiento preventivo del sistema de Circuito Cerrado de Televisi??n para "+nombre+" en el area del "+str(area_de_mantenimiento)+" ubicada en "+lugar_de_mantenimiento, styleN)
        #cambios 
        p7extra2 = Paragraph("Para aplicar el mantenimiento preventivo es importante que el sistema se encuentre en operaci??n, sin fallas, de lo contrario se aplicar??a un mantenimiento correctivo y despu??s proceder??a el preventivo.", styleN)
        p7extra3 = Paragraph("Se considera una p??liza de mantenimiento preventivo con duraci??n de 12 Meses", styleN)
        pblank = Paragraph("""<para> <br/> </para>""")
        p8 = Paragraph("??ndice de propuesta:, ", styleN)
        p9 = Paragraph("1.0 Antecedentes.", styleN)
        p10 = Paragraph("2.0 Alcances de los trabajos.", styleN)
        p11 = Paragraph("3.0 Precio y Formas de Pago.", styleN)
        p12 = Paragraph("4.0 Precio fuera del contrato de mantenimiento.", styleN)
        pAntecedentes1 = Paragraph("""<u>1.0 Antecedentes</u>""", styleB)
        pAntecedentes2 = Paragraph("Los dispositivos en total considerados a mantenimento son los siguientes:",styleN)
        listdisp = [["Dispositivo","Cantidad",Paragraph("Visitas por a??o"),Paragraph("Visitas adicionales por a??o"),Paragraph("Dispositivos en periodicidad adcional")]]
        mantenimientos = Mantenimiento_CCTV.objects.filter(cliente = cliente_id,cotizacion=cotizacion_id)
        for mantenimiento in mantenimientos:
            if mantenimiento.periodisidadadicional is not None or mantenimiento.periodisidadadicional != 0:
                if mantenimiento.dispositivo is not None:
                    if mantenimiento.periodisidadadicional is None:
                        info_disp = [Paragraph(mantenimiento.dispositivo),mantenimiento.cantidaddedispositivos,mantenimiento.periodisidadactividades,0,0]
                    else:    
                        info_disp = [Paragraph(mantenimiento.dispositivo),mantenimiento.cantidaddedispositivos,mantenimiento.periodisidadactividades,mantenimiento.periodisidadadicional,mantenimiento.cantidaddispositivosextras]
                    listdisp.append(info_disp)
            else:
                if mantenimiento.dispositivo is not None:
                    info_disp = [Paragraph(mantenimiento.dispositivo),mantenimiento.cantidaddedispositivos]
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

        titulo = Nombre_servicio_CCTV.objects.get(pk=5)
        totaldisp = Mantenimiento_CCTV.objects.get(titulonombre = titulo,cotizacion=cotizacion_id,cliente=cliente_id)
        titulofirmware = Nombre_servicio_CCTV.objects.get(pk=7)
        totaldispfirmware = Mantenimiento_CCTV.objects.get(titulonombre = titulofirmware,cotizacion=cotizacion_id,cliente=cliente_id)
        titulosoftware = Nombre_servicio_CCTV.objects.get(pk=21)
        totaldispsoftware = Mantenimiento_CCTV.objects.get(titulonombre = titulosoftware,cotizacion=cotizacion_id,cliente=cliente_id)
        pAntecedentes3 = Paragraph("Total de dispositivos: "+str(totaldisp.cantidaddedispositivos), styleN)
        pAntecedentes4 = Paragraph("Total de dispositivos con update de Firmware: "+str(totaldispfirmware.cantidaddedispositivos), styleN)
        pAntecedentes5 = Paragraph("Total de dispositivos con update de Licencia de Software: "+str(totaldispsoftware.cantidaddedispositivos), styleN)
        
        palcances0 = Paragraph("""<u>2.0 Alcances de los trabajos</u>""",styleB)
        palcances1 = Paragraph("Alcances de trabajo del mantenimeinto preventivo:",styleN)
        palcances2 = Paragraph("""<u>??Qu?? se incluye?:</u>""",styleB)
        meses = int(12 / cotizacion.periodoregular)
        if cotizacion.periodoregular == 1:
            palcances3 = Paragraph("De manera calendarizada se ejecutar?? la limpieza de los equipos mencionados anteriormente cada {} meses con un total de {} evento por a??o.".format(meses,cotizacion.periodoregular),styleN,bulletText="1.")
        else:
            palcances3 = Paragraph("De manera calendarizada se ejecutar?? la limpieza de los equipos mencionados anteriormente cada {} meses con un total de {} eventos por a??o.".format(meses,cotizacion.periodoregular),styleN,bulletText="1.")
        palcances4 = Paragraph("Limpieza de Equipos grabadores de Video",styleN,bulletText="2.")
        palcances5 = Paragraph("Limpieza de todos los dispositivos de CCTV.",styleN,bulletText="3.")
        palcances6 = Paragraph("Revisi??n de la transmisi??n de video en tiempo real al monitor.",styleN,bulletText="4.")
        palcances7 = Paragraph("Revisi??n del video del monitor, se verifica que tenga buen brillo y contraste.",styleN,bulletText="5.")
        palcances8 = Paragraph("Revisi??n de las fuentes de poder y su funcionamiento.",styleN,bulletText="6.")
        palcances9 = Paragraph("De ser detectado un dispositivo da??ado, los costos asociados ser??n cotizados de manera independiente e instalados previa autorizaci??n del cliente.",styleN,bulletText="7.")
        palcances10 = Paragraph("Alcances de trabajo del mantenimiento de emergencia:",styleN,bulletText="8.")
        palcances11 = Paragraph("Soporte T??cnico 5 d??as a la semana (lunes a viernes de 8:00am a 5:00pm).",styleN,bulletText="???")
        
        suma_horas = 0
        for mantenimiento in mantenimientos:
            if str(mantenimiento.titulonombre) == "Servicio de soporte t??cnico -Horas de servicios generales adicionales":
                suma_horas = mantenimiento.tiempoejecucion
        suma_horas_palabra = num2words(suma_horas,lang='es')
        
        palcances12 = Paragraph(str(suma_horas)+" horas de servicio t??cnico anual o 12 meses, lo que suceda primero para atenci??n a fallas en sitio.",styleN,bulletText="???")
        palcances13 = Paragraph("Servicios de reparaci??n, diagn??sticos, ajustes y actualizaciones.",styleN,bulletText="???")
        palcances15 = Paragraph("Actualizaci??n de Firmware de Dispositivos de c??maras, NVR.",styleN,bulletText="???")
        palcances16 = Paragraph("En su caso Limpieza de estaci??n de trabajo (PC) Cliente y servidor de visualizaci??n.",styleN,bulletText="???")
        palcances17 = Paragraph("""<u>??Qu?? se excluye?:</u>""",styleB)
        palcances18= Paragraph("Actualizaci??n de sistemas operativos o parches en Estaciones de trabajo y servidores.",styleN,bulletText="1.")
        palcances19= Paragraph("Refacciones como cables, c??maras, fuentes, nvr. (en caso de necesitarse se cotizaran por escrito y ser??n instaladas previa autorizaci??n del cliente).",styleN,bulletText="2.")
        palcances20= Paragraph("Maquinaria de Elevaci??n si no se se??ala que esta considerada dentro del costo.",styleN,bulletText="3.")
        
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


        table_dis = Table(listdisp,colWidths=[3*inch,1*inch,1*inch , 1*inch])
        ts = TableStyle([("GRID",(0,0),(-1,-1),2,colors.black)])
        table_dis.setStyle(ts)

        td_mantenimientos = [["Mantenimiento",Paragraph("Acts. de mmnto por a??o"),
                            Paragraph("Acts. adicionales")
                            ,Paragraph("Tiempo de ejecucion")]]
        for mantenimiento in mantenimientos:
            if str(mantenimiento.titulonombre) != "Servicio de soporte t??cnico -Horas de servicios generales adicionales":
                if mantenimiento.periodisidadadicional is None:
                    data_mantenimientos = [Paragraph(str(mantenimiento.titulonombre)),mantenimiento.periodisidadactividades,0,mantenimiento.tiempoejecucion]
                else:
                    data_mantenimientos = [Paragraph(str(mantenimiento.titulonombre)),mantenimiento.periodisidadactividades,mantenimiento.periodisidadadicional,mantenimiento.tiempoejecucion]  
                    td_mantenimientos.append(data_mantenimientos)

            elif str(mantenimiento.titulonombre) == "Servicio de soporte t??cnico -Horas de servicios generales adicionales":
                costohorasservicio = mantenimiento.costototal

        table_man = Table(td_mantenimientos,colWidths=[3*inch,1*inch,1*inch , 1*inch])
        table_man.setStyle(ts)

        td_total = [["Total de horas de servicio de soporte t??cnico incluidas en esta poliza","Horas",suma_horas]]
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
        preciofinaltexto = "${:,.2f}".format(preciofinal)
        preciofinalincadicionalnum = float(round(preciofinalincadicional))
        preciofinalincadicional1 = num2words(preciofinalincadicional, to="currency", lang='es', currency='USD').upper()
        preciofinalincadicional = "${:,.2f}".format(preciofinalincadicionalnum)
        
        ts_pre = TableStyle([("GRID",(0,0),(-1,-1),2,colors.black),
                             ("BACKGROUND",(0,0),(-1,0),colors.lightsteelblue)])
        td_precio = [["Descripcion","Cantidad","Unidad","Costo"]]
        td_precioadicional = [["Descripcion","Cantidad","Unidad","Costo"]]

        data_precio = [Paragraph("Cuota anual del contrato de  mantenimiento"), Paragraph("1",styleNC),Paragraph("Lot",styleNC),Paragraph("{}".format(preciofinaltexto),styleNC)]
        data_precioadicional = [Paragraph("Cuota anual del contrato de  mantenimiento incluyendo periodicidad adicional"), Paragraph("1",styleNC),Paragraph("Lot",styleNC),Paragraph("{}".format(preciofinalincadicional),styleNC)]
        td_precio.append(data_precio)

        preciommto = preciofinal - costohorasservicio
        preciommto = float(round(preciommto))
        costohorasservicio = float(round(costohorasservicio))
        table_pre = Table(td_precio)
        table_pre.setStyle(ts_pre)
        ppreciotexto = Paragraph(preciofinal1+" USD + IVA",styleNBC)
        
        pprecio1 = Paragraph("""<u>3.0 Precio y forma de pago:</u>""",styleB)
        pprecio2 = Paragraph("Mantenimiento preventivo de equipos:             $ {} USD".format(preciommto),styleN)
        pprecio3 = Paragraph("Horas de Servicios de emergencia de equipos:     $ {} USD".format(costohorasservicio),styleN)
        pprecio4 = Paragraph("Precio total por mantenimiento anual",styleN)
        pprecio6 = Paragraph("""<u>Precio total por mantenimiento anual pagadero por evento          $ {} USD</u>""".format(preciofinal),styleCB)
        pprecio7 = Paragraph("El pago es cada evento, debe estar liquidado antes de efectuarse el mantenimiento.",styleNC)
        
        if cotizacion.periodoregular == 1:
            preciocuatri = float(round(preciofinal))
            pprecio8 = Paragraph("Pago anual en una sola exhibicion: $ {} Dlls + IVA".format(preciocuatri),styleN)
        elif cotizacion.periodoregular == 2:
            preciocuatri = float(round(preciofinal/2))
            pprecio8 = Paragraph("Pago anual en dos exhibiciones:  $ {} Dlls + IVA".format(preciocuatri),styleN)
        elif cotizacion.periodoregular == 3:
            preciocuatri = float(round(preciofinal/3))
            pprecio8 = Paragraph("Pago anual en tres exhibiciones:  $ {} Dlls + IVA".format(preciocuatri),styleN)
        elif cotizacion.periodoregular == 4:
            preciocuatri = float(round(preciofinal/4))
            pprecio8 = Paragraph("Pago anual en cuatro exhibiciones:  $ {} Dlls + IVA".format(preciocuatri),styleN)
        elif cotizacion.periodoregular == 6:
            preciocuatri = float(round(preciofinal/6))
            pprecio8 = Paragraph("Pago anual en seis exhibiciones:  $ {} Dlls + IVA".format(preciocuatri),styleN)
        
        preciocuatritexto = num2words(preciocuatri, to="currency", lang='es', currency='USD')
        pprecio9 = Paragraph("({} d??lares mas IVA)".format(preciocuatritexto),styleN)
        
        #Precio para mantenimientos con periodicidad adicional
        listmanteniminientos = []
        for mantenimiento in mantenimientos:
            if mantenimiento.costomantenimientoadicional != 0 and mantenimiento.costomantenimientoadicional != None:
                listmanteniminientos.append(mantenimiento.costomantenimientoadicional)
        if any(listmanteniminientos):
            pprecioadicional1 = Paragraph("Precio total por mantenimiento anual incluyendo periodicidades adicionales",styleN)
            pprecioadicional2 = Paragraph("""<u>Precio total por mantenimiento anual pagadero por evento incluyendo periodicidades adicionales          {} USD</u>""".format(preciofinalincadicional),styleCB)
            pprecioadicional3 = Paragraph("El pago es cada evento, debe estar liquidado antes de efectuarse el mantenimiento.",styleNC)
            precioadicionalcuatritexto = num2words(preciofinalincadicionalnum, to="currency", lang='es', currency='USD')        
            
            if cotizacion.periodoregular == 1:
                precioadicionalcuatri = preciofinalincadicionalnum
                pprecioadicional14 = Paragraph("Pago anual en una sola exhibicion: $ {} Dlls + IVA".format(precioadicionalcuatri),styleN)
            elif cotizacion.periodoregular == 2:
                precioadicionalcuatri = preciofinalincadicionalnum/2
                pprecioadicional14 = Paragraph("Pago anual en dos exhibiciones: $ {} Dlls + IVA".format(precioadicionalcuatri),styleN)
            elif cotizacion.periodoregular == 3:
                precioadicionalcuatri = preciofinalincadicionalnum/3
                pprecioadicional14 = Paragraph("Pago anual en tres exhibiciones: $ {} Dlls + IVA".format(precioadicionalcuatri),styleN)
            elif cotizacion.periodoregular == 4:
                precioadicionalcuatri = preciofinalincadicionalnum/4
                pprecioadicional14 = Paragraph("Pago anual en cuatro exhibiciones: $ {} Dlls + IVA".format(precioadicionalcuatri),styleN)
            elif cotizacion.periodoregular == 6:
                precioadicionalcuatri = preciofinalincadicionalnum/6
                pprecioadicional14 = Paragraph("Pago anual en seis exhibiciones: $ {} Dlls + IVA".format(precioadicionalcuatri),styleN)
            
            pprecioadicional15 = Paragraph("({} d??lares mas IVA)".format(precioadicionalcuatritexto),styleN)
        
        pprecio10 = Paragraph("""<u>Condiciones Comerciales:</u>""",styleB)
        pprecio11 = Paragraph("Los precios arriba mencionados son expresados en D??lares Americanos y no incluye IVA.",styleN,bulletText="???")
        pprecio12 = Paragraph("Para proceder con el servicio es necesario estar cubierta la p??liza el primer d??a del mes que se realizara el mantenimiento. ",styleN,bulletText="???")
        pprecio13 = Paragraph("Si se realiza el pago en pesos su tipo de cambio ser?? en relaci??n a la instituci??n bancaria de compra de banco Santander o BBVA  confirmar antes.",styleN,bulletText="???")

        
        pterminos0 = Paragraph("""<u>4.0 Precio fuera del contrato de mantenimiento:</u>""",styleB)
        pterminos1 = Paragraph("Los costos por hora en horario de 8am a 5pm es de $65.00 DLL por hora por t??cnico.",styleN,bulletText="1.")
        pterminos2 = Paragraph("Los costos por hora en horario de 8:00 am a 5:00 pm es de $126.00 DLL por hora por ingeniero.",styleN,bulletText="2.")
        pterminos3 = Paragraph("El costo por hora en estos horarios es de $90.00 USD por t??cnico y $190.00 USD por ingeniero: Lunes a viernes de 6:00pm a 7am, S??bados de 1pm a 11:59pm, Domingos de las 00:00 a 11:59pm Los costos de servicio de facturan desde la visita para la revisi??n, an??lisis, identificaci??n del problema y soluci??n. ",styleN,bulletText="3.")
        pterminos4 = Paragraph("Soporte v??a telef??nica para apoyo a personal de {} para la atenci??n de un evento el cual vacilen en poder solucionarlos, se les apoya 30 minutos en caso de no resolverse se env??a un t??cnico al sitio a costo adicional para el cliente. Costo de soporte t??cnico v??a telef??nica $35.50 USD por evento. Horario de soporte t??cnico de 8:00am a 5:00 Pm sin n??mero de emergencias.".format(cliente),styleN,bulletText="4.")
        pterminos5 = Paragraph("En caso de falla de los dispositivos y se tenga que reemplazar el equipo, El costo reflejado ser?? el tiempo asociado del personal t??cnico en evaluaci??n y diagnostico , mas el costo de las refacciones mas costos de envi?? si aplican en garant??as, devoluciones, etc.",styleN,bulletText="5.")
        pterminos6 = Paragraph("Los precios arriba mencionados son expresados en D??lares americanos y no incluye IVA. ",styleN,bulletText="-")
        pterminos7 = Paragraph("La facturaci??n en servicios se presenta por evento. ",styleN,bulletText="-")
        pterminos8 = Paragraph("Sin m??s por el momento y en espera para cualquier aclaraci??n al respecto, quedo de usted. ",styleN,bulletText="-")
        pterminosatentamente = Paragraph("Atentamente",styleNC)

        info = InformacionPersonal.objects.get(user=usuario)
        nombrecontitulo = str(info.titulo)+"."+" "+str(info.nombre)+" "+str(info.apellido)
        puesto = str(info.puesto)
        pfin = Paragraph("Fin del documento",styleNC)
        pregards = Paragraph("Regards",styleNC)
        pnombrecontitulo = Paragraph(nombrecontitulo,styleNC)
        ppuesto = Paragraph(puesto,styleNC)
        
        
        #Portada
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
        Story.append(p7extra2)
        Story.append(pblank)
        Story.append(p7extra3)
        Story.append(pblank)
        Story.append(p8)
        Story.append(p9)
        Story.append(p10)
        Story.append(p11)
        Story.append(p12)
        Story.append(PageBreak())

        #1.0 Antecedentes
        Story.append(pAntecedentes1)
        Story.append(pAntecedentes2)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(table_dis)
        Story.append(pblank)
        Story.append(pAntecedentes3)
        Story.append(pAntecedentes4)
        Story.append(pAntecedentes5)
        Story.append(pblank)
        Story.append(PageBreak())

        #2.0 Alcances de los trabajos
        Story.append(palcances0)
        Story.append(pblank)
        Story.append(palcances1)
        Story.append(pblank)
        Story.append(palcances2)
        Story.append(pblank)
        Story.append(palcances3)
        Story.append(palcances4)
        Story.append(palcances5)
        Story.append(palcances6)
        Story.append(palcances7)
        Story.append(palcances8)
        Story.append(palcances9)
        Story.append(palcances10)
        Story.append(Indenter("1cm"))
        Story.append(palcances11)
        Story.append(palcances12)
        Story.append(palcances13)
        Story.append(palcances15)
        Story.append(palcances16)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(Indenter("-1cm"))
        Story.append(palcances17)
        Story.append(pblank)
        Story.append(palcances18)
        Story.append(palcances19)
        Story.append(palcances20)
        Story.append(pblank)
        Story.append(PageBreak())

        #3.0 Precio y forma de pago
        Story.append(pprecio1)
        Story.append(pblank)
        Story.append(pprecio2)
        Story.append(pprecio3)
        Story.append(pblank)
        Story.append(pprecio4)
        Story.append(pblank)
        Story.append(pprecio6)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pprecio7)
        Story.append(pblank)
        Story.append(pprecio8)
        Story.append(pprecio9)
        Story.append(pblank)
        if any(listmanteniminientos):
            Story.append(pblank)
            Story.append(pprecioadicional1)
            Story.append(pblank)
            Story.append(pprecioadicional2)
            Story.append(pblank)
            Story.append(pprecioadicional3)
            Story.append(pblank)
            Story.append(pprecioadicional14)
            Story.append(pprecioadicional15)
            Story.append(pblank)
        Story.append(pprecio10)
        Story.append(pblank)
        Story.append(pprecio11)
        Story.append(pprecio12)
        Story.append(pprecio13)
        Story.append(pblank)
        Story.append(PageBreak())

        #4.0 precio fuera del contrato
        Story.append(pterminos0)
        Story.append(pblank)
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
        Story.append(pterminosatentamente)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pnombrecontitulo)
        Story.append(ppuesto)





        doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
        # doc.build(Story)
    go()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True,  filename='cotizacion_cctv_{}.pdf'.format(nombre))

def cotizacion_pdf_ca(request, cliente_id,cotizacion_id,usuario):

    cliente = Cliente.objects.get(pk=cliente_id)
    cotizacion = Cotizacion_CA.objects.get(pk=cotizacion_id,cliente=cliente_id)
    # mantenimientos = Cliente.mantenimiento.through.objects.
    buf = io.BytesIO()

    nombre=cliente.nombre
    lugar_de_mantenimiento = cotizacion.lugar_de_mantenimiento
    descripcion_cotizacion = cotizacion.descripcion_cotizacion

    locale.setlocale(locale.LC_TIME, 'es-ES')
    dateTimeObj = datetime.now()
    dateStr = dateTimeObj.strftime("%d de %B del %Y ")

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
                              leading=12,
                              ))
    styles.add(ParagraphStyle(name='Normal_J',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_JUSTIFY,
                              fontSize=10,
                              textColor=colors.black,
                              leading=15,))
    styles.add(ParagraphStyle(name='Normal_C',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.black,
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Right',
                              parent=styles['Normal'],
                              wordWrap='LTR',
                              alignment=TA_RIGHT,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              leading=12,))

    styles.add(ParagraphStyle(name='Heading1_B',
                              parent=styles['Heading1'],
                              wordWrap='LTR',
                              alignment=TA_LEFT,
                              fontSize=12,
                              textColor=colors.HexColor("#3498DB"),
                              leading=12,))
    styles.add(ParagraphStyle(name='Heading1_BC',
                              parent=styles['Heading1'],
                              wordWrap='LTR',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.HexColor("#3498DB"),
                              leading=12,))

    styles.add(ParagraphStyle(name='Normal_CB',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_B',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_LEFT,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Red',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_LEFT,
                              fontSize=12,
                              textColor=colors.red,
                              fontName="Helvetica-bold",
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Ye',
                              parent=styles['Normal'],
                              wordWrap='CJK',
                              alignment=TA_CENTER,
                              fontSize=12,
                              textColor=colors.black,
                              fontName="Helvetica-bold",
                              backColor = colors.yellow,
                              leading=12,))
    styles.add(ParagraphStyle(name='Normal_Center',
                            parent=styles['Normal'],
                            wordWrap='CJK',
                            alignment=TA_CENTER,
                            fontSize=12,
                            textColor=colors.black,
                            fontName="Helvetica-bold",
                            leading=12,))


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
        mantenimientos = Mantenimiento_CA.objects.filter(cliente = cliente_id,cotizacion=cotizacion_id)
        for mantenimiento in mantenimientos:
            listdisp = []
            listdisp.append(mantenimiento.dispositivo)
        cliente = Cliente.objects.get(pk=cliente_id)
        cotizacion = Cotizacion_CA.objects.get(pk=cotizacion_id,cliente=cliente_id)
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
        p6 = Paragraph("Estimados se??ores, ", styleN)
        p7 = Paragraph("En relaci??n a su solicitud presentamos los costos asociados del servicio de mantenimiento preventivo del sistema de Control de Accesos para "+nombre+" ubicada en "+lugar_de_mantenimiento, styleN)
        p7extra2 = Paragraph("Para aplicar el mantenimiento preventivo es importante que el sistema se encuentre en operaci??n, sin fallas, de lo contrario se aplicar??a un mantenimiento correctivo y despu??s proceder??a el preventivo.", styleN)
        p7extra3 = Paragraph("Se considera una p??liza de mantenimiento preventivo con duraci??n de 12 Meses", styleN)
        pblank = Paragraph("""<para> <br/> </para>""")
        p8 = Paragraph("??ndice de propuesta:, ", styleN)
        p9 = Paragraph("1.0 Antecedentes.", styleN)
        p10 = Paragraph("2.0 Alcances de los trabajos.", styleN)
        p11 = Paragraph("3.0 Precio y Formas de Pago.", styleN)
        p12 = Paragraph("4.0 Precio fuera del contrato de mantenimiento.", styleN)
        pAntecedentes1 = Paragraph("""<u>1.0 Antecedentes</u>""", styleB)
        pAntecedentes2 = Paragraph("Los dispositivos en total considerados a mantenimento son los siguientes:",styleN)
        listdisp = [["Dispositivo","Cantidad",Paragraph("Visitas por a??o"),Paragraph("Visitas adicionales por a??o"),Paragraph("Dispositivos en periodicidad adcional")]]
        mantenimientos = Mantenimiento_CA.objects.filter(cliente = cliente_id,cotizacion=cotizacion_id)
        for mantenimiento in mantenimientos:
            if mantenimiento.periodisidadadicional is not None or mantenimiento.periodisidadadicional != 0:
                if mantenimiento.dispositivo is not None:
                    if mantenimiento.periodisidadadicional is None:
                        info_disp = [Paragraph(mantenimiento.dispositivo),mantenimiento.cantidaddedispositivos,mantenimiento.periodisidadactividades,0,0]
                    else:    
                        info_disp = [Paragraph(mantenimiento.dispositivo),mantenimiento.cantidaddedispositivos,mantenimiento.periodisidadactividades,mantenimiento.periodisidadadicional,mantenimiento.cantidaddispositivosextras]
                    listdisp.append(info_disp)
            else:
                if mantenimiento.dispositivo is not None:
                    info_disp = [Paragraph(mantenimiento.dispositivo),mantenimiento.cantidaddedispositivos]
                    listdisp.append(info_disp)

        # listadispositivos = ''
        # lastdisp = listdisp[-1]

        # for mantenimiento in mantenimientos:
        #     if len(listdisp) == 1:
        #         if mantenimiento.dispositivo is not None:
        #             listadispositivos = listadispositivos+" "+str(mantenimiento.cantidaddedispositivos)+" "+str(mantenimiento.dispositivo)+'.'
            
        #     elif mantenimiento.dispositivo != lastdisp:
        #         if mantenimiento.dispositivo is not None:
        #             listadispositivos = listadispositivos+" "+str(mantenimiento.cantidaddedispositivos)+" "+str(mantenimiento.dispositivo)+","
                
        #     else:
        #         if mantenimiento.dispositivo is not None:
        #             listadispositivos = listadispositivos+" "+str(mantenimiento.cantidaddedispositivos)+" "+str(mantenimiento.dispositivo)+","
        #             listadispositivos = listadispositivos[:-1]
        #             listadispositivos = listadispositivos+"."

        titulo = Nombre_servicio_CA.objects.get(pk=1)
        totaldisp = Mantenimiento_CA.objects.get(titulonombre = titulo,cotizacion=cotizacion_id,cliente=cliente_id)
        titulofirmware = Nombre_servicio_CA.objects.get(pk=3)
        totaldispfirmware = Mantenimiento_CA.objects.get(titulonombre = titulofirmware,cotizacion=cotizacion_id,cliente=cliente_id)
        pAntecedentes3 = Paragraph("Total de dispositivos: "+str(totaldisp.cantidaddedispositivos), styleN)
        pAntecedentes4 = Paragraph("Total de dispositivos con update de firmware: "+str(totaldispfirmware.cantidaddedispositivos), styleN)
        
        palcances0 = Paragraph("""<u>2.0 Alcances de los trabajos</u>""",styleB)
        palcances1 = Paragraph("Alcances de trabajo del mantenimiento preventivo:",styleN)
        palcances2 = Paragraph("""<u>??Qu?? se incluye?:</u>""",styleB)
        meses = int(12 / cotizacion.periodoregular)
        if cotizacion.periodoregular == 1:
            palcances3 = Paragraph("De manera calendarizada se ejecutar?? la limpieza de los equipos mencionados anteriormente cada {} meses con un total de {} evento por a??o.".format(meses,cotizacion.periodoregular),styleN,bulletText="???")
        else:
            palcances3 = Paragraph("De manera calendarizada se ejecutar?? la limpieza de los equipos mencionados anteriormente cada {} meses con un total de {} eventos por a??o.".format(meses,cotizacion.periodoregular),styleN,bulletText="???")
        palcances4 = Paragraph("Limpieza de Pc, estaciones de trabajo y servidores.",styleN,bulletText="???")
        palcances5 = Paragraph("Limpieza de Fuentes de poder y controladoras, m??dulos y gabinetes.",styleN,bulletText="???")
        palcances6 = Paragraph("Revisi??n de sus comunicaciones IP y RS-485.",styleN,bulletText="???")
        palcances7 = Paragraph("Revisi??n del video del monitor, se verifica que tenga buen brillo y contraste.",styleN,bulletText="???")
        palcances8 = Paragraph("Revisi??n de las bater??as, m??dulos y rectificadores de las fuentes de poder.",styleN,bulletText="???")
        palcances9 = Paragraph("Actualizaci??n de Software administrador de accesos  y firmware en equipos controladores.",styleN,bulletText="???")
        palcances10 = Paragraph("Actualizaci??n de software de nuevos service pack o cambio de versiones en Sistema operativo.",styleN,bulletText="???")
        palcances11 = Paragraph("Pruebas de comunicaci??n de datos de los equipos PC, servidores y controladores.",styleN,bulletText="???")
        palcances12 = Paragraph("Implementaci??n de actualizaciones a la versi??n actual, cambios de versi??n y pruebas para software de administraci??n y monitoreo.",styleN,bulletText="???")
        palcances13 = Paragraph("Ajustes y correcciones de los accesorios de las puertas como bot??n de salida, magnetos, lectoras, sensores de estado de las puertas.",styleN,bulletText="???")
        palcances14 = Paragraph("Verificaci??n de correcta operaci??n de la integraci??n con control de elevadores y en su caso correcciones necesarias.",styleN,bulletText="???")
        palcances15 = Paragraph("Verificaci??n y actualizaciones de correlaciones entre puertas de accesos y canal de video asociado.",styleN,bulletText="???")
        palcances16 = Paragraph("Soporte T??cnico 5 d??as a la semana (lunes a viernes de 8:00am a 5:00pm).",styleN,bulletText="???")

        suma_horas = 0
        for mantenimiento in mantenimientos:
            if str(mantenimiento.titulonombre) == "Servicio de soporte t??cnico -Horas de servicios generales adicionales":
                suma_horas = mantenimiento.tiempoejecucion
        suma_horas_palabra = num2words(suma_horas,lang='es')
        
        palcances17 = Paragraph(str(suma_horas)+" horas de servicio t??cnico anual o 12 meses, lo que suceda primero para atenci??n a fallas en sitio.",styleN,bulletText="???")
        palcances18 = Paragraph("""<u>??Qu?? se excluye?:</u>""",styleB)
        palcances19= Paragraph("No incluye maquinaria de elevaci??n, de ser necesaria ser?? cotizada de manera independiente.",styleN,bulletText="???")
        palcances20= Paragraph("No se Incluye refacciones.",styleN,bulletText="???")
        palcances21= Paragraph("Nota: De ser detectado un dispositivo da??ado, los costos asociados ser??n cotizados de manera independiente e instalados previa autorizaci??n del cliente, en caso de aplicar garant??a no tendr?? costo m??s que los asociados por envi?? y retorno a el fabricante.",styleN)
        
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


        ppolitica12 = Paragraph("Tiempo de  Programaci??n y configuraci??n de Paneles  sobre los equipos dentro de la p??liza de mantenimiento.",styleN,bulletText="???")
        #ppolitica13 = Paragraph("Tarjetas loops, panel, estrobos, sensores fotoel??ctricos, fuentes de poder, m??dulos de control. Monitores de flujo, resistencias de fin de l??nea.",styleN,bulletText="-")
        ppolitica14 = Paragraph("Atenci??n a Emergencias en caso de falla total del panel principal y que la operaci??n del 50% o mas del sistema este comprometida con un tiempo de respuesta en sitio de 4 hora.",styleN,bulletText="???")
        ppolitica16 = Paragraph("Los costos asociados de un dispositivo da??ado ser?? tomado en cuenta de la lista de precios que se proporciona en este documento en conjunto con el contrato, de esta manera cuando un dispositivo se da??en la facturaci??n de la refacci??n sea en base a este precio.",styleN)



        table_dis = Table(listdisp,colWidths=[3*inch,1*inch,1*inch , 1*inch])
        ts = TableStyle([("GRID",(0,0),(-1,-1),2,colors.black)])
        table_dis.setStyle(ts)

        td_mantenimientos = [["Mantenimiento",Paragraph("Acts. de mmnto por a??o"),
                            Paragraph("Acts. adicionales")
                            ,Paragraph("Tiempo de ejecucion")]]
        for mantenimiento in mantenimientos:
            if str(mantenimiento.titulonombre) != "Servicio de soporte t??cnico -Horas de servicios generales adicionales":
                if mantenimiento.periodisidadadicional is None:
                    data_mantenimientos = [Paragraph(str(mantenimiento.titulonombre)),mantenimiento.periodisidadactividades,0,mantenimiento.tiempoejecucion]
                else:
                    data_mantenimientos = [Paragraph(str(mantenimiento.titulonombre)),mantenimiento.periodisidadactividades,mantenimiento.periodisidadadicional,mantenimiento.tiempoejecucion]
                td_mantenimientos.append(data_mantenimientos)
            elif str(mantenimiento.titulonombre) == "Servicio de soporte t??cnico -Horas de servicios generales adicionales":
                costohorasservicio = mantenimiento.costototal

        table_man = Table(td_mantenimientos,colWidths=[3*inch,1*inch,1*inch , 1*inch])
        table_man.setStyle(ts)

        td_total = [["Total de horas de servicio de soporte t??cnico incluidas en esta poliza","Horas",suma_horas]]
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
        preciofinaltexto = "${:,.2f}".format(preciofinal)
        preciofinalincadicionalnum = float(round(preciofinalincadicional))
        preciofinalincadicional1 = num2words(preciofinalincadicional, to="currency", lang='es', currency='USD').upper()
        preciofinalincadicional = "${:,.2f}".format(preciofinalincadicionalnum)

        ts_pre = TableStyle([("GRID",(0,0),(-1,-1),2,colors.black),
                             ("BACKGROUND",(0,0),(-1,0),colors.lightsteelblue)])
        td_precio = [["Descripcion","Cantidad","Unidad","Costo"]]
        td_precioadicional = [["Descripcion","Cantidad","Unidad","Costo"]]

        data_precio = [Paragraph("Cuota anual del contrato de  mantenimiento"), Paragraph("1",styleNC),Paragraph("Lot",styleNC),Paragraph("{}".format(preciofinal),styleNC)]
        data_precioadicional = [Paragraph("Cuota anual del contrato de  mantenimiento incluyendo periodicidad adicional"), Paragraph("1",styleNC),Paragraph("Lot",styleNC),Paragraph("{}".format(preciofinalincadicional),styleNC)]
        td_precio.append(data_precio)

        costohorasservicio = float(round(costohorasservicio))  
        preciommto = preciofinal - costohorasservicio
        preciommto = float(round(preciommto))
        costohorasservicio = float(round(costohorasservicio))   
        table_pre = Table(td_precio)
        table_pre.setStyle(ts_pre)
        ppreciotexto = Paragraph(preciofinal1+" USD + IVA",styleNBC)
        pprecio1 = Paragraph("""<u>3.0 Precio y forma de pago:</u>""",styleB)
        pprecio2 = Paragraph("Mantenimiento preventivo de equipos:             $ {} USD".format(preciommto),styleN)
        pprecio3 = Paragraph("Horas de Servicios de emergencia de equipos:     $ {} USD".format(costohorasservicio),styleN)
        pprecio4 = Paragraph("Precio total por mantenimiento anual",styleN)
        pprecio6 = Paragraph("""<u>Precio total por mantenimiento anual pagadero por evento          $ {} USD</u>""".format(preciofinal),styleCB)
        pprecio7 = Paragraph("El pago es cada evento, debe estar liquidado antes de efectuarse el mantenimiento.",styleNC)
                
        if cotizacion.periodoregular == 1:
            preciocuatri = float(round(preciofinal))
            pprecio8 = Paragraph("Pago anual en una sola exhibicion: $ {} Dlls + IVA".format(preciocuatri),styleN)
        elif cotizacion.periodoregular == 2:
            preciocuatri = float(round(preciofinal/2))
            pprecio8 = Paragraph("Pago anual en dos exhibiciones:  $ {} Dlls + IVA".format(preciocuatri),styleN)
        elif cotizacion.periodoregular == 3:
            preciocuatri = float(round(preciofinal/3))
            pprecio8 = Paragraph("Pago anual en tres exhibiciones:  $ {} Dlls + IVA".format(preciocuatri),styleN)
        elif cotizacion.periodoregular == 4:
            preciocuatri = float(round(preciofinal/4))
            pprecio8 = Paragraph("Pago anual en cuatro exhibiciones:  $ {} Dlls + IVA".format(preciocuatri),styleN)
        elif cotizacion.periodoregular == 6:
            preciocuatri = float(round(preciofinal/6))
            pprecio8 = Paragraph("Pago anual en seis exhibiciones:  $ {} Dlls + IVA".format(preciocuatri),styleN)
        
        preciocuatritexto = num2words(preciocuatri, to="currency", lang='es', currency='USD')
        pprecio9 = Paragraph("({} d??lares mas IVA)".format(preciocuatritexto),styleN)
        
        #Precio para mantenimientos con periodicidad adicional
        listmanteniminientos = []
        for mantenimiento in mantenimientos:
            if mantenimiento.costomantenimientoadicional != 0 and mantenimiento.costomantenimientoadicional != None:
                listmanteniminientos.append(mantenimiento.costomantenimientoadicional)
        if any(listmanteniminientos):
            pprecioadicional1 = Paragraph("Precio total por mantenimiento anual incluyendo periodicidades adicionales",styleN)
            pprecioadicional2 = Paragraph("""<u>Precio total por mantenimiento anual pagadero por evento incluyendo periodicidades adicionales          {} USD</u>""".format(preciofinalincadicional),styleCB)
            pprecioadicional3 = Paragraph("El pago es cada evento, debe estar liquidado antes de efectuarse el mantenimiento.",styleNC)
            precioadicionalcuatritexto = num2words(preciofinalincadicionalnum, to="currency", lang='es', currency='USD')        
            
            if cotizacion.periodoregular == 1:
                precioadicionalcuatri = float(round(preciofinalincadicionalnum))
                pprecioadicional14 = Paragraph("Pago anual en una sola exhibicion: $ {} Dlls + IVA".format(precioadicionalcuatri),styleN)
            elif cotizacion.periodoregular == 2:
                precioadicionalcuatri = float(round(preciofinalincadicionalnum/2))
                pprecioadicional14 = Paragraph("Pago anual en dos exhibiciones: $ {} Dlls + IVA".format(precioadicionalcuatri),styleN)
            elif cotizacion.periodoregular == 3:
                precioadicionalcuatri = float(round(preciofinalincadicionalnum/3))
                pprecioadicional14 = Paragraph("Pago anual en tres exhibiciones: $ {} Dlls + IVA".format(precioadicionalcuatri),styleN)
            elif cotizacion.periodoregular == 4:
                precioadicionalcuatri = float(round(preciofinalincadicionalnum/4))
                pprecioadicional14 = Paragraph("Pago anual en cuatro exhibiciones: $ {} Dlls + IVA".format(precioadicionalcuatri),styleN)
            elif cotizacion.periodoregular == 6:
                precioadicionalcuatri = float(round(preciofinalincadicionalnum/6))
                pprecioadicional14 = Paragraph("Pago anual en seis exhibiciones: $ {} Dlls + IVA".format(precioadicionalcuatri),styleN)
            
            pprecioadicional15 = Paragraph("({} d??lares mas IVA)".format(precioadicionalcuatritexto),styleN)
        
        pprecio10 = Paragraph("""<u>Condiciones Comerciales:</u>""",styleB)
        pprecio11 = Paragraph("Los precios arriba mencionados son expresados en D??lares Americanos y no incluye IVA.",styleN,bulletText="???")
        pprecio12 = Paragraph("Para proceder con el servicio es necesario estar cubierta la p??liza el primer d??a del mes que se realizara el mantenimiento. ",styleN,bulletText="???")
        pprecio13 = Paragraph("Si se realiza el pago en pesos su tipo de cambio ser?? en relaci??n a la instituci??n bancaria de compra de banco Santander o BBVA confirmar antes.",styleN,bulletText="???")

        
        pterminos0 = Paragraph("""<u>4.0 Precio fuera del contrato de mantenimiento:</u>""",styleB)
        pterminos1 = Paragraph("Los costos por hora en horario de 8am a 5pm es de $66.00 DLL por hora por t??cnico.",styleN,bulletText="1.")
        pterminos2 = Paragraph("Los costos por hora en horario de 8:00 am a 5:00 pm es de $135.00 DLL por hora por ingeniero.",styleN,bulletText="2.")
        pterminos3 = Paragraph("El costo por hora en estos horarios es de $90.00 USD por t??cnico y $190.00 USD por ingeniero: ",styleN,bulletText="3.")
        pterminos4 = Paragraph("Lunes a viernes de 6:00pm a 7am",styleN)
        pterminos5 = Paragraph("S??bados de 1pm a 11:59pm ",styleN)
        pterminos6 = Paragraph("Domingos de las 00:00 a 11:59pm",styleN)
        pterminos7 = Paragraph("Los costos de servicio de facturan desde la visita para la revisi??n, an??lisis, identificaci??n del problema y soluci??n.",styleN)
        pterminos8 = Paragraph("Soporte v??a telef??nica para apoyo a personal de {} para la atenci??n de un evento el cual vacilen en poder solucionarlos, se les apoya 30 minutos en caso de no resolverse se env??a un t??cnico al sitio a costo adicional para el cliente. Costo de soporte t??cnico v??a telef??nica $35.50 USD por evento. Horario de soporte t??cnico de 8:00am a 5:00 Pm sin n??mero de emergencias.".format(cliente),styleN,bulletText="4.")
        pterminos9 = Paragraph("En caso de falla de los dispositivos y se tenga que reemplazar el equipo, El costo reflejado ser?? el tiempo asociado del personal t??cnico involucrado, refacciones + costos de envi?? si aplican en garant??as, devoluciones, etc.",styleN,bulletText="5.")
        pterminos10 = Paragraph("Los precios arriba mencionados son expresados en D??lares americanos y no incluye IVA.",styleN)
        pterminosatentamente = Paragraph("Atentamente",styleNC)
        
        if cotizacion.periodoregular == 1:
            pextra1 = Paragraph("La facturaci??n del mantenimiento anual se presentar?? en una exhibicion anual y ser?? pagadera antes de la fecha de ejecuci??n del evento de mantenimiento.",styleN)
        elif cotizacion.periodoregular == 2:
            pextra1 = Paragraph("La facturaci??n del mantenimiento anual se presentar?? en dos exhibiciones semestrales y ser?? pagadera antes de la fecha de ejecuci??n del evento de  mantenimiento.",styleN)
        elif cotizacion.periodoregular == 3:
            pextra1 = Paragraph("La facturaci??n del mantenimiento anual se presentar?? en tres exhibiciones cuatrimestrales y ser?? pagadera antes de la fecha de ejecuci??n del evento de  mantenimiento.",styleN)        
        elif cotizacion.periodoregular == 4:
            pextra1 = Paragraph("La facturaci??n del mantenimiento anual se presentar?? en cuatro exhibiciones trimestrales y ser?? pagadera antes de la fecha de ejecuci??n del evento de  mantenimiento.",styleN)
        elif cotizacion.periodoregular == 6:
            pextra1 = Paragraph("La facturaci??n del mantenimiento anual se presentar?? en seis exhibiciones bimestrales y ser?? pagadera antes de la fecha de ejecuci??n del evento de  mantenimiento.",styleN)
        
        pextra2 = Paragraph("La facturaci??n en servicios fuera de p??liza se presenta por evento. ",styleN)
        pextra3 = Paragraph("Sin m??s por el momento y en espera para cualquier aclaraci??n al respecto, quedo de usted.",styleN)

        info = InformacionPersonal.objects.get(user=usuario)
        nombrecontitulo = str(info.titulo)+"."+" "+str(info.nombre)+" "+str(info.apellido)
        puesto = str(info.puesto)
        pfin = Paragraph("Fin del documento",styleNC)
        pregards = Paragraph("Regards",styleNC)
        pnombrecontitulo = Paragraph(nombrecontitulo,styleNC)
        ppuesto = Paragraph(puesto,styleNC)
        
        #Portada
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
        Story.append(pblank)
        Story.append(p7extra2)
        Story.append(pblank)
        Story.append(p7extra3)
        Story.append(pblank)
        Story.append(p8)
        Story.append(p9)
        Story.append(p10)
        Story.append(p11)
        Story.append(p12)
        Story.append(PageBreak())

        #1.0 Antecedentes
        Story.append(pAntecedentes1)
        Story.append(pAntecedentes2)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(table_dis)
        Story.append(pblank)
        Story.append(pAntecedentes3)
        Story.append(pAntecedentes4)
        Story.append(pblank)
        Story.append(PageBreak())

        #2.0 Alcances de los trabajos
        Story.append(palcances0)
        Story.append(pblank)
        Story.append(palcances1)
        Story.append(pblank)
        Story.append(palcances2)
        Story.append(pblank)
        Story.append(palcances3)
        Story.append(palcances4)
        Story.append(palcances5)
        Story.append(palcances6)
        Story.append(palcances7)
        Story.append(palcances8)
        Story.append(palcances9)
        Story.append(palcances10)
        Story.append(palcances11)
        Story.append(palcances12)
        Story.append(palcances13)
        Story.append(palcances14)
        Story.append(palcances15)
        Story.append(palcances16)
        Story.append(palcances17)
        Story.append(pblank)
        Story.append(palcances18)
        Story.append(pblank)
        Story.append(palcances19)
        Story.append(palcances20)
        Story.append(pblank)
        Story.append(palcances21)
        Story.append(pblank)
        Story.append(PageBreak())

        #3.0 Precio y forma de pago
        Story.append(pprecio1)
        Story.append(pblank)
        Story.append(pprecio2)
        Story.append(pprecio3)
        Story.append(pblank)
        Story.append(pprecio4)
        Story.append(pblank)
        Story.append(pprecio6)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pprecio7)
        Story.append(pblank)
        Story.append(pprecio8)
        Story.append(pprecio9)
        Story.append(pblank)
        if any(listmanteniminientos):
            Story.append(pblank)
            Story.append(pprecioadicional1)
            Story.append(pblank)
            Story.append(pprecioadicional2)
            Story.append(pblank)
            Story.append(pprecioadicional3)
            Story.append(pblank)
            Story.append(pprecioadicional14)
            Story.append(pprecioadicional15)
            Story.append(pblank)
        Story.append(pprecio10)
        Story.append(pblank)
        Story.append(pprecio11)
        Story.append(pprecio12)
        Story.append(pprecio13)
        Story.append(pblank)
        Story.append(PageBreak())

        #4.0 precio fuera del contrato
        Story.append(pterminos0)
        Story.append(pblank)
        Story.append(pterminos1)
        Story.append(pterminos2)
        Story.append(pterminos3)
        Story.append(pterminos4)
        Story.append(pterminos5)
        Story.append(pterminos6)
        Story.append(pterminos7)
        Story.append(pterminos8)
        Story.append(pterminos9)
        Story.append(pterminos10)
        Story.append(pblank)
        Story.append(pextra1)
        Story.append(pextra2)
        Story.append(pextra3)
        Story.append(pblank)
        Story.append(pfin)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pterminosatentamente)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pblank)
        Story.append(pnombrecontitulo)
        Story.append(ppuesto)

        doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
        # doc.build(Story)
    go()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True,  filename='cotizacion_ca_{}.pdf'.format(nombre))




# Create your views here.
