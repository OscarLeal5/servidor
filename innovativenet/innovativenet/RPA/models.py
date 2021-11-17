import dateutil
from django.db import models
from django.contrib.auth.models import User
from dateutil import utils
from django.db.models import Sum

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
        # Se guarda la cotizacion primero
        super(Cotizacion, self).save(*args, **kwargs)
        # Se almacena en una variable la lista de todos los nombres de mantenimientos
        opciones = Nombre_servicio.objects.all()
        # Ciclo para agregar automaticamente los mantenimientos por medio de los nombres que estan almacenados en Nombre_Servicio
        for opcion in opciones:
            # Se declaran los valores que se quieren tener en todos los mantenimientos
            Mantenimiento.objects.create(titulonombre=opcion,cotizacion=self,cliente=self.cliente,periodisidadactividades=self.periodoregular,
            periodisidadadicional=self.periodoadicional)
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
                # 13 es el pk del titulo cambiar herramientas
                if self.titulonombre == Nombre_servicio.objects.get(pk=13):
                    # Se guarda en una variable la lista de mantenimientos excluyendo el de Cambiar herramientas
                    todoslosservicios = Mantenimiento.objects.filter(cliente=self.cliente,cotizacion=self.cotizacion)
                    # Se obtienen las cantidades de dispositivos regulares y adicionales excluyendo los mantenimientos que sean de Ingeniero
                    todoslosservicios = todoslosservicios.exclude(titulonombre=Nombre_servicio.objects.get(pk=13))
                    totalperiodoadicional = todoslosservicios.exclude(encargadoTrabajo1=Precio.objects.get(encargado='Ingeniero')).aggregate(periodo_adicional=Sum('periodisidadadicional'))
                    # Se iguala al valor de la suma 
                    totalperiodoadicional = totalperiodoadicional["periodo_adicional"] 
                    # Se checa si el total de la periodicidad adicional es nulo o igual a cero
                    if totalperiodoadicional is None or totalperiodoadicional == 0 :
                        # Si es igual a nulo o cero realiza esto
                        # Despues checa si el valor del mantenimiento de cambiar herramientas es nulo o cero
                        if self.periodisidadadicional is None or self.periodisidadadicional == 0:
                            # Si es igual a nulo o cero realiza esto
                            # Iguala las variables a cero para que no haya problemas al realizar operaciones numericas
                            self.cantidaddispositivosextras = 0
                            self.costomantenimientoadicional = 0
                            # Realiza la suma de la cantidad de dispositivos regulares de todos los servicios
                            totaldispositivosregular = todoslosservicios.aggregate(Sum('cantidaddedispositivos'))
                            totaldispositivosregular = totaldispositivosregular['cantidaddedispositivos__sum']
                            # Se igualan las variables a los valores dentro de Nombre_Servicio
                            self.encargadoTrabajo1 = titulo.encargado
                            self.tiempoejecucion = titulo.tiempodeejecucion
                            # Se iguala el valor del mantenimiento al total de los dipositivos
                            self.cantidaddedispositivos = totaldispositivosregular
                            # Si el valor de dispositivos es Nulo se iguala a cero para no tener problemas al hacer operaciones numericas
                            if self.cantidaddedispositivos == None:
                                self.cantidaddedispositivos = 0
                            # Se calcula el valor del total de horas de actividad regular
                            self.horasactividad = self.tiempoejecucion * self.cantidaddedispositivos
                            # Se calcula el costo regular del mantenimiento
                            self.costomantenimientoregular = self.encargadoTrabajo1.precio * self.horasactividad
                            # Se calcula el costo total sumando el costo regular y el costo adicional
                            self.costototal = self.costomantenimientoadicional + self.costomantenimientoregular
                            # Si la periodicidad es nulo o cero se iguala a Nulo la cantidad de dispositivos adicionales
                            if self.periodisidadadicional is None or 0:    
                                self.cantidaddispositivosextras = None
                            return super(Mantenimiento, self).save(*args, **kwargs)
                    else:
                        # Se igualan variables a cero para que se puedan hacer calculos numericos sin problema
                        totaldispositivosregular = 0
                        totaldispositivosregular = 0
                        # Se guarda en una variable la lista de mantenimientos excluyendo el de Cambiar herramientas
                        todoslosservicios = todoslosservicios.exclude(titulonombre=Nombre_servicio.objects.get(pk=13))
                        # Se obtienen las cantidades de dispositivos regulares y adicionales excluyendo los mantenimientos que sean de Ingeniero
                        totaldispositivosregular = todoslosservicios.exclude(encargadoTrabajo1=Precio.objects.get(encargado='Ingeniero')).aggregate(cantidad_disp=Sum('cantidaddedispositivos'))
                        totaldispositivosadicional = todoslosservicios.exclude(encargadoTrabajo1=Precio.objects.get(encargado='Ingeniero')).aggregate(cantidad_disp_adi=Sum('cantidaddispositivosextras'))
                        # Asignar variable al total de dispositivos regulares y adicionales
                        totaldispositivosregular = totaldispositivosregular['cantidad_disp']
                        totaldispositivosadicional = totaldispositivosadicional['cantidad_disp_adi']
                        # Se igualan variables a valores que esten en Base de datos de Nombre_Servicio
                        self.encargadoTrabajo1 = titulo.encargado
                        self.tiempoejecucion = titulo.tiempodeejecucion
                        # Se asigna las variables con las de la base de datos Nombre_Servicio
                        self.cantidaddedispositivos = totaldispositivosregular
                        self.cantidaddispositivosextras = totaldispositivosadicional
                        # Se calcular el total de horas de actividad regular
                        self.horasactividad = self.tiempoejecucion * self.cantidaddedispositivos
                        # Se calcular el total de horas de actividad adicional
                        self.horasactividadadicional = self.tiempoejecucion * self.cantidaddispositivosextras
                        # Se calcula el costo total de mantenimientos de la periodicidad regular
                        self.costomantenimientoregular = self.encargadoTrabajo1.precio * self.horasactividad
                        # Se calcula el costo total de mantenimientos de la periodicidad adicional
                        self.costomantenimientoadicional = self.tiempoejecucion * self.cantidaddispositivosextras 
                        self.costomantenimientoadicional = self.costomantenimientoadicional * self.encargadoTrabajo1.precio
                        # Se calcula el costo total sumando el costo regular y el adicional
                        self.costototal = self.costomantenimientoadicional + self.costomantenimientoregular
                        super(Mantenimiento, self).save(*args, **kwargs)
                        return
                    
                # Se checa si el titulo del mantenimiento que se esta guardando con los titulos de la base de datos de Nombre_Servicio
                # y tambien con que sea distinto al titulo de Cambiar Herramientas
                elif str(self.titulonombre) == titulo.titulo and self.titulonombre != Nombre_servicio.objects.get(pk=13):
                    # Si la vairbale es igual a Null va a igualar las siguientes variables a cero para hacer calculos con valores numericos
                    if self.periodisidadadicional is None:
                        self.cantidaddispositivosextras = 0
                        self.periodisidadadicional = 0
                    # Se asigna las variables con las de la base de datos Nombre_Servicio
                    self.encargadoTrabajo1 = titulo.encargado
                    self.tiempoejecucion = titulo.tiempodeejecucion
                    self.dispositivo = titulo.dispositivo
                    # Se calculan las horas de actividad regular multiplicando el timepo de ejecucion del servicio con la cantidad de dispositivos regulares
                    self.horasactividad = self.tiempoejecucion * self.cantidaddedispositivos
                    # Se obtiene el costo regular multiplicando las horas de actividad obtenidas en el paso anterior con el precio del encargado de dicho mantenimiento
                    self.costomantenimientoregular = self.encargadoTrabajo1.precio * self.horasactividad
                    # Calcula las horas de actividad adicional multiplicando tiempo de ejecucion del servicio con la cantidad de dispositivos adicionales registrados
                    self.horasactividadadicional = self.tiempoejecucion * self.cantidaddispositivosextras
                    # Se calcula un pre valor de costo adicional multiplicando el tiempo de ejecucion por cantidad de 
                    # dispositivos adicionales registrados por las periodicidades adicionales registradas
                    self.costomantenimientoadicional = self.tiempoejecucion * self.cantidaddispositivosextras * self.periodisidadadicional
                    # Se obtiene el costo adicional multiplicando las horas de actividad obtenidas en el paso anterior con el precio del encargado de dicho mantenimiento
                    self.costomantenimientoadicional = self.costomantenimientoadicional * self.encargadoTrabajo1.precio
                    # Calcular el costo total sumando los valores del costo regular y costo adicional
                    self.costototal = self.costomantenimientoregular + self.costomantenimientoadicional
                    # Se regresan los valores a Null para que sigan los valores originales de la base de datos
                    if self.periodisidadadicional == 0:
                        self.cantidaddispositivosextras = None
                        self.periodisidadadicional = None
                    # Se manda llamar la funcion superior de save del modelo, es decir es el save original del modelo.
                    super(Mantenimiento, self).save(*args, **kwargs)
                    # Se manda llamar la funcion total_cambio
                    Mantenimiento.total_cambio(self)
                    return
                elif str(self.titulonombre) == titulo.titulo and self.titulonombre != Nombre_servicio.objects.get(pk=13) and self.encargadoTrabajo1 == Precio.objects.get(encargado='Ingeniero'):
                    # Si la vairbale es igual a Null va a igualar las siguientes variables a cero para hacer calculos con valores numericos
                    if self.periodisidadadicional is None:
                        self.cantidaddispositivosextras = 0
                        self.periodisidadadicional = 0
                    # Se asigna las variables con las de la base de datos Nombre_Servicio
                    self.encargadoTrabajo1 = titulo.encargado
                    self.tiempoejecucion = titulo.tiempodeejecucion
                    self.dispositivo = titulo.dispositivo
                    self.cantidaddedispositivos = self.periodisidadactividades
                    self.cantidaddispositivosextras = self.periodisidadadicional
                    # Se calculan las horas de actividad regular multiplicando el timepo de ejecucion del servicio con la cantidad de dispositivos regulares
                    self.horasactividad = self.tiempoejecucion * self.cantidaddedispositivos
                    # Se obtiene el costo regular multiplicando las horas de actividad obtenidas en el paso anterior con el precio del encargado de dicho mantenimiento
                    self.costomantenimientoregular = self.encargadoTrabajo1.precio * self.horasactividad
                    # Calcula las horas de actividad adicional multiplicando tiempo de ejecucion del servicio con la cantidad de dispositivos adicionales registrados
                    self.horasactividadadicional = self.tiempoejecucion * self.cantidaddispositivosextras
                    # Se calcula un pre valor de costo adicional multiplicando el tiempo de ejecucion por cantidad de 
                    # dispositivos adicionales registrados por las periodicidades adicionales registradas
                    self.costomantenimientoadicional = self.tiempoejecucion * self.cantidaddispositivosextras * self.periodisidadadicional
                    # Se obtiene el costo adicional multiplicando las horas de actividad obtenidas en el paso anterior con el precio del encargado de dicho mantenimiento
                    self.costomantenimientoadicional = self.costomantenimientoadicional * self.encargadoTrabajo1.precio
                    # Calcular el costo total sumando los valores del costo regular y costo adicional
                    self.costototal = self.costomantenimientoregular + self.costomantenimientoadicional
                    # Se regresan los valores a Null para que sigan los valores originales de la base de datos
                    if self.periodisidadadicional == 0:
                        self.cantidaddispositivosextras = None
                        self.periodisidadadicional = None
                    # Se manda llamar la funcion superior de save del modelo, es decir es el save original del modelo.
                    super(Mantenimiento, self).save(*args, **kwargs)
                    # Se manda llamar la funcion total_cambio
                    Mantenimiento.total_cambio(self)
                    return


# Funcion para calcular el total de dispositivos cada que se actualiza un mantenimiento
    def total_cambio(self):
        # Se obtiene el titulo de cambio de herramientas
        titulo = Nombre_servicio.objects.get(pk=13)
        # Se busca o crea el mantenimiento con el titulo, cotizacion y cliente que se este actualizando
        Mantenimiento.objects.get_or_create(cotizacion=self.cotizacion,cliente=self.cliente,titulonombre=titulo)
        # Se busca el mantenimiento creado y se almacena en una variable
        cambio = Mantenimiento.objects.get(cotizacion=self.cotizacion,cliente=self.cliente,titulonombre=titulo)
        # Se manda llamar la funcion save para guardar y recalcular el total de dispositivos
        cambio.save()
        return 

    def __str__(self):
        return str(self.titulonombre)

    class Meta:
        ordering = ['encargadoTrabajo1','cantidaddedispositivos']

        