import dateutil
from django.db import models
from django.contrib.auth.models import User
from dateutil import utils
from django.db.models import Sum, Count

from django.db.models.fields import NullBooleanField

class Precio(models.Model):
    encargado = models.CharField(max_length=50, verbose_name='Encargado del trabajo',blank=True, null=True)
    precio = models.FloatField("Precio por hora",blank=True, null=True)

    def __str__(self):
        return self.encargado
    class Meta:
        ordering = ['encargado']

class Nombre_servicio(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Titulo Mantenimiento", null=True, blank=True)
    encargado = models.ForeignKey(Precio, on_delete=models.CASCADE, null=True)
    tiempodeejecucion = models.FloatField(verbose_name="Tiempo de Ejecucion", null=True)
    dispositivo = models.CharField(max_length=200, verbose_name="Dispositivo al que se le aplica el mantenimiento", null=True, blank=True)
    def __str__(self):
        return str(self.titulo)
    
    class Meta:
        ordering = ['titulo']
    
class Cliente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField('Nombre de la compañia cliente',max_length=200)
    encargado = models.CharField('Nombre del contacto dentro de la empresa',max_length
    =120)
    puesto_encargado = models.CharField('Puesto del contacto',max_length
    =120)
    numero_contacto=models.CharField('Numero de telefono para contactar',max_length
    =10)
    correo_contacto=models.EmailField('Correo para contactar',blank=True)
    

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']

class Cotizacion(models.Model):
    num_list = [(1,"1"),(2,"2"),(4,"4"),(6,"6")]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField(verbose_name="Nombre Cotizacion", null=True, blank=True,max_length=200)
    lugar_de_mantenimiento = models.CharField('Lugar en que se realizara el mantenimiento',max_length
    =120,blank=True)
    descripcion_cotizacion = models.TextField('Descripcion de la cotizacion',blank=True)
    fecha = models.DateTimeField('Fecha de realizacion de la cotizacion',blank=True,null=True, default=dateutil.utils.today())
    periodoregular = models.IntegerField('Periodicidad regular de mmto al año',choices=num_list,null=True)
    preguntaperiodoadicional = models.BooleanField('Quieres agregar periodicidad adicional a la regular?',default=False)
    periodoadicional=models.IntegerField('Periodicidad adicional a la regular',choices=num_list,null=True,blank=True)
    mantenimientos = models.ManyToManyField(Nombre_servicio,through="Mantenimiento")

    def save(self, *args, **kwargs):
        super(Cotizacion, self).save(*args, **kwargs)
        opciones = Nombre_servicio.objects.all()
        for opcion in opciones:
            Mantenimiento.objects.create(titulonombre=opcion,cotizacion=self,cliente=self.cliente,periodisidadactividades=self.periodoregular,
            periodisidadadicional=self.periodoadicional)
            # self.mantenimientos.add(nuevo,through_defaults={'tiempoejecucion':opcion.tiempodeejecucion,'cotizacion':self,'cliente':self.cliente,'periodisidadactividades':self.periodoregular,'periodisidadadicional':self.periodoadicional})
        super(Cotizacion, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.cliente)+"-"+str(self.titulo)

    class Meta:
        ordering = ['cliente']


class Mantenimiento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, null=True, blank=True)
    titulonombre = models.ForeignKey(Nombre_servicio,on_delete=models.CASCADE, null=True, blank=True)
    encargadoTrabajo1 = models.ForeignKey(Precio,verbose_name="Encargado del trabajo" ,on_delete=models.CASCADE,null=True)
    periodisidadactividades = models.IntegerField(verbose_name="Periodicidad regular de actividad de mtto por año", blank=True, null=True )
    periodisidadadicional = models.IntegerField(verbose_name="Periodicidad adicional de actividad de mtto  a la regular", blank=True, null=True)
    tiempoejecucion = models.FloatField(verbose_name="Tiempo de ejecucion del mtto", blank=True, null=True)
    cantidaddedispositivos = models.IntegerField(verbose_name="Cantidad de dispositivos a considerar en periodicidad regular", blank=True, null=True,default=0)
    cantidaddispositivosextras = models.IntegerField(verbose_name="Cantidad de dispositivos a considerar en periodicidad Extra", blank=True, null=True,default=0)
    horasactividad = models.FloatField(verbose_name="horas por actividad de mtto regular =Importe de cantidad x Tiempo de ejecucion", blank=True, null=True)
    horasactividadadicional = models.FloatField(verbose_name="horas por actividad de mtto adicional =Importe de cantidad x Tiempo de ejecucion", blank=True, null=True)
    costomantenimientoregular = models.FloatField(verbose_name="Costo Regular = horas por actividad de mtto regular =Importe de cantidad x Tiempo de ejecucion",null=True,blank=True)
    costomantenimientoadicional = models.FloatField(verbose_name="Costo Adicional = horas por actividad de mtto adicional =Importe de cantidad x Tiempo de ejecucion ", blank=True, null=True)
    costototal = models.FloatField(verbose_name="Costo total = Costo regular + costo adicional",null=True,blank=True)
    dispositivo = models.CharField("Dispositivo al que se le da mantenimiento",null=True,blank=True,max_length=200)

    def save(self, *args, **kwargs):
            # Para los titulos dentro de la base de datos Nombre_Servicio
            for titulo in Nombre_servicio.objects.all():
                # Se busca el titulo que sea equivalente al titulo en Nombre_Servicio
                #13 es el pk del titulo cambiar herramientas
                if self.titulonombre == Nombre_servicio.objects.get(pk=13):
                    print("entro al if de cambiar herramientas")
                    todoslosservicios = Mantenimiento.objects.filter(cliente=self.cliente,cotizacion=self.cotizacion)
                    todoslosservicios = todoslosservicios.exclude(titulonombre=Nombre_servicio.objects.get(pk=13))
                    todoslosservicios = todoslosservicios.exclude(encargadoTrabajo1=Precio.objects.get(encargado='Ingeniero'))
                    totalperiodoadicional = todoslosservicios.aggregate(Sum('periodisidadadicional'))
                    totalperiodoadicional = totalperiodoadicional["periodisidadadicional__sum"] 
                    if totalperiodoadicional is None or totalperiodoadicional == 0 :
                        print("entro al if de totalperiodoadicional")
                        if self.periodisidadadicional is None or self.periodisidadadicional == 0:
                            print("entro al if de self.periodisidadadicional")
                            self.cantidaddispositivosextras = 0
                            self.costomantenimientoadicional = 0
                            totaldispositivosregular = todoslosservicios.aggregate(Sum('cantidaddedispositivos'))
                            totaldispositivosregular = totaldispositivosregular['cantidaddedispositivos__sum']
                            self.encargadoTrabajo1 = titulo.encargado
                            self.tiempoejecucion = titulo.tiempodeejecucion
                            self.cantidaddedispositivos = totaldispositivosregular
                            print(totaldispositivosregular)
                            # totaldispositivos = self.cantidaddispositivosextras + self.cantidaddedispositivos
                            if self.cantidaddedispositivos == None:
                                self.cantidaddedispositivos = 0
                            self.horasactividad = self.tiempoejecucion * self.cantidaddedispositivos
                            self.costomantenimientoregular = self.encargadoTrabajo1.precio * self.horasactividad
                            self.costototal = self.costomantenimientoadicional + self.costomantenimientoregular
                            if self.periodisidadadicional is None or 0:    
                                self.cantidaddispositivosextras = None
                            return super(Mantenimiento, self).save(*args, **kwargs)
                    else:
                        print("entro al else de totalperiodicidad")
                        totaldispositivosregular = 0
                        totaldispositivosregular = 0
                        todoslosservicios = todoslosservicios.exclude(titulonombre=Nombre_servicio.objects.get(pk=13))
                        totaldispositivosregular = todoslosservicios.exclude(encargadoTrabajo1=Precio.objects.get(encargado='Ingeniero')).aggregate(cantidad_disp=Sum('cantidaddedispositivos'))
                        totaldispositivosadicional = todoslosservicios.exclude(encargadoTrabajo1=Precio.objects.get(encargado='Ingeniero')).aggregate(cantidad_disp_adi=Sum('cantidaddispositivosextras'))
                        totaldispositivosregular = totaldispositivosregular['cantidad_disp']
                        totaldispositivosadicional = totaldispositivosadicional['cantidad_disp_adi']
                        self.encargadoTrabajo1 = titulo.encargado
                        self.tiempoejecucion = titulo.tiempodeejecucion
                        self.cantidaddedispositivos = totaldispositivosregular
                        self.cantidaddispositivosextras = totaldispositivosadicional
                        # totaldispositivos = self.cantidaddispositivosextras + self.cantidaddedispositivos
                        self.horasactividad = self.tiempoejecucion * self.cantidaddedispositivos
                        self.horasactividadadicional = self.tiempoejecucion * self.cantidaddispositivosextras
                        self.costomantenimientoregular = self.encargadoTrabajo1.precio * self.horasactividad
                        self.costomantenimientoadicional = self.tiempoejecucion * self.cantidaddispositivosextras 
                        self.costomantenimientoadicional = self.costomantenimientoadicional * self.encargadoTrabajo1.precio
                        self.costototal = self.costomantenimientoadicional + self.costomantenimientoregular
                        super(Mantenimiento, self).save(*args, **kwargs)
                        return
                    
                elif str(self.titulonombre) == titulo.titulo and self.titulonombre != Nombre_servicio.objects.get(pk=13):
                    # se asigna las variables con las de la base de datos Nombre_Servicio
                    print("\n\nencontro Servicio\n\n")
                    if self.periodisidadadicional is None:
                        self.cantidaddispositivosextras = 0
                        self.periodisidadadicional = 0
                    self.encargadoTrabajo1 = titulo.encargado
                    self.tiempoejecucion = titulo.tiempodeejecucion
                    self.dispositivo = titulo.dispositivo
                    # Se calculan las horas de actividad regular multiplicando el timepo de ejecucion del servicio con la cantidad de dispositivos regulares
                    self.horasactividad = self.tiempoejecucion * self.cantidaddedispositivos
                    # Se obtiene el costo regular multiplicando las horas de actividad obtenidas en el paso anterior con el precio del encargado de dicho mantenimiento
                    self.costomantenimientoregular = self.encargadoTrabajo1.precio * self.horasactividad
                    #calcula las horas de actividad adicional multiplicando tiempo de ejecucion del servicio con la cantidad de dispositivos adicionales registrados
                    self.horasactividadadicional = self.tiempoejecucion * self.cantidaddispositivosextras
                    # Se calcula un pre valor de costo adicional multiplicando el tiempo de ejecucion por cantidad de 
                    # dispositivos adicionales registrados por las periodicidades adicionales registradas
                    self.costomantenimientoadicional = self.tiempoejecucion * self.cantidaddispositivosextras * self.periodisidadadicional
                    # Se obtiene el costo adicional multiplicando las horas de actividad obtenidas en el paso anterior con el precio del encargado de dicho mantenimiento
                    self.costomantenimientoadicional = self.costomantenimientoadicional * self.encargadoTrabajo1.precio
                    #Calcular el costo total sumando los valores del costo regular y costo adicional
                    self.costototal = self.costomantenimientoregular + self.costomantenimientoadicional
                    if self.periodisidadadicional == 0:
                        self.cantidaddispositivosextras = None
                        self.periodisidadadicional = None
                    super(Mantenimiento, self).save(*args, **kwargs)
                    Mantenimiento.total_cambio(self)
                    return

    def total_cambio(self):
                print("prueba")
                titulo = Nombre_servicio.objects.get(pk=13)
                Mantenimiento.objects.get_or_create(cotizacion=self.cotizacion,cliente=self.cliente,titulonombre=titulo)
                cambio = Mantenimiento.objects.get(cotizacion=self.cotizacion,cliente=self.cliente,titulonombre=titulo)
                cambio.save()
                return 

    def __str__(self):
        return str(self.titulonombre)

    class Meta:
        ordering = ['encargadoTrabajo1']

        
class Dispositivo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    marca = models.CharField(max_length=200, verbose_name="Marca del dispositivo", null=True, blank=True)
    titulo = models.CharField(max_length=200, verbose_name="Nombre del dispositivo", null=True, blank=True)
    cantidad = models.IntegerField(verbose_name="Cantidad de dispositivos actuales", null=True)
    actividad = models.CharField(max_length=200, verbose_name="Actividad de mantenimiento a realizar",null=True, blank=True)
    plan = models.CharField(max_length=200, verbose_name="Tipo de poliza/plan", null=True, blank=True)

    def __str__(self):
        return self.titulo
    class Meta:
        ordering = ['titulo']