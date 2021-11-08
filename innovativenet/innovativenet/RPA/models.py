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
    #dispositivo = models.CharField(max_length=200, verbose_name="Dispositivo al que se le aplica el mantenimiento", null=True, blank=True)
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
    cantidaddedispositivos = models.IntegerField(verbose_name="Cantidad de dispositivos a considerar en periodicidad regular", blank=True, null=True,default=1)
    cantidaddispositivosextras = models.IntegerField(verbose_name="Cantidad de dispositivos a considerar en periodicidad Extra", blank=True, null=True,default=1)
    horasactividad = models.FloatField(verbose_name="horas por actividad de mtto regular =Importe de cantidad x Tiempo de ejecucion", blank=True, null=True)
    horasactividadadicional = models.FloatField(verbose_name="horas por actividad de mtto adicional =Importe de cantidad x Tiempo de ejecucion", blank=True, null=True)
    costomantenimientoregular = models.FloatField(verbose_name="Costo Regular = horas por actividad de mtto regular =Importe de cantidad x Tiempo de ejecucion",null=True,blank=True)
    costomantenimientoadicional = models.FloatField(verbose_name="Costo Adicional = horas por actividad de mtto adicional =Importe de cantidad x Tiempo de ejecucion ", blank=True, null=True)
    
    def total_cambio(self):
                print("prueba")
                titulo = Nombre_servicio.objects.get(pk=13)
                cambio = Mantenimiento.objects.get(cotizacion=self.cotizacion,cliente=self.cliente,titulonombre=titulo)
                return cambio.save()

    def save(self, *args, **kwargs):
            # Para los titulos dentro de la base de datos Nombre_Servicio
            for titulo in Nombre_servicio.objects.all():
                # Se busca el titulo que sea equivalente al titulo en Nombre_Servicio
                if str(self.titulonombre) == titulo.titulo and self.titulonombre != Nombre_servicio.objects.get(pk=13):
                    # se asigna las variables con las de la base de datos Nombre_Servicio
                    print("\n\nencontro Servicio\n\n")
                    if self.periodisidadadicional is None:
                        self.cantidaddispositivosextras = 0
                    self.encargadoTrabajo1 = titulo.encargado
                    self.tiempoejecucion = titulo.tiempodeejecucion
                    # Se obtienen varioles finales con variables previamente asignadas por medio de multiplicaciones.
                    self.horasactividad = self.tiempoejecucion * self.cantidaddedispositivos
                    self.horasactividadadicional = self.tiempoejecucion * self.cantidaddispositivosextras
                    self.costomantenimientoadicional = self.tiempoejecucion * self.cantidaddispositivosextras * self.periodisidadadicional
                    self.costomantenimientoadicional = self.costomantenimientoadicional * self.encargadoTrabajo1.precio
                    self.costomantenimientoregular = self.encargadoTrabajo1.precio * self.horasactividad
                    super(Mantenimiento, self).save(*args, **kwargs)
                    Mantenimiento.total_cambio(self)
                    return

                #13 es el pk del titulo cambiar herramientas
                elif self.titulonombre == Nombre_servicio.objects.get(pk=13):
                    todoslosservicios = Mantenimiento.objects.filter(cliente=self.cliente,cotizacion=self.cotizacion)
                    todoslosservicios = todoslosservicios.exclude(encargadoTrabajo1=Precio.objects.get(encargado='Ingeniero'))
                    todoslosservicios = todoslosservicios.exclude(titulonombre=Nombre_servicio.objects.get(pk=13))
                    totalperiodoadicional = todoslosservicios.aggregate(Sum('periodisidadadicional'))
                    totalperiodoadicional = totalperiodoadicional["periodisidadadicional__sum"] 
                    if totalperiodoadicional is None:
                        if self.periodisidadadicional is None:
                            self.cantidaddispositivosextras = 0
                            totaldispositivosregular = todoslosservicios.aggregate(Sum('cantidaddedispositivos'))
                            totaldispositivosregular = totaldispositivosregular['cantidaddedispositivos__sum']
                            self.encargadoTrabajo1 = titulo.encargado
                            self.tiempoejecucion = titulo.tiempodeejecucion
                            self.cantidaddedispositivos = totaldispositivosregular
                            print(totaldispositivosregular)
                            totaldispositivos = self.cantidaddispositivosextras + self.cantidaddedispositivos
                            self.horasactividad = self.tiempoejecucion * self.cantidaddedispositivos
                            super(Mantenimiento, self).save(*args, **kwargs)
                            return
                    else:
                        print(totalperiodoadicional)
                        totaldispositivosregular = todoslosservicios.aggregate(Sum('cantidaddedispositivos'))
                        totaldispositivosadicional = todoslosservicios.aggregate(Sum('cantidaddispositivosextras'))
                        totaldispositivosregular = totaldispositivosregular['cantidaddedispositivos__sum']
                        totaldispositivosadicional = totaldispositivosadicional['cantidaddispositivosextras__sum']
                        self.encargadoTrabajo1 = titulo.encargado
                        self.tiempoejecucion = titulo.tiempodeejecucion
                        self.cantidaddedispositivos = totaldispositivosregular
                        self.cantidaddispositivosextras = totaldispositivosadicional
                        totaldispositivos = self.cantidaddispositivosextras + self.cantidaddedispositivos
                        self.horasactividad = self.tiempoejecucion * self.cantidaddedispositivos
                        self.horasactividadadicional = self.tiempoejecucion * self.cantidaddispositivosextras
                        super(Mantenimiento, self).save(*args, **kwargs)
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