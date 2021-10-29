from django.db import models
from django.contrib.auth.models import User
import dateutil.utils

class Precio(models.Model):
    encargado = models.CharField(max_length=50, verbose_name='Encargado del trabajo',blank=True, null=True)
    precio = models.FloatField("Precio por hora",blank=True, null=True)

    def __str__(self):
        return self.encargado
    class Meta:
        ordering = ['encargado']

class Dispositivo(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Nombre del dispositivo", null=True, blank=True)
    cantidad = models.IntegerField(verbose_name="Cantidad de dispositivos actuales", null=True)
    actividad = models.CharField(max_length=200, verbose_name="Actividad de mantenimiento a realizar",null=True, blank=True)
    plan = models.CharField(max_length=200, verbose_name="Tipo de poliza/plan", null=True, blank=True)

    def __str__(self):
        return self.titulo
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
    lugar_de_mantenimiento = models.CharField('Lugar en que se realizara el mantenimiento',max_length
    =120,blank=True)
    descripcion_cotizacion = models.TextField('Descripcion de la cotizacion',blank=True)
    fecha = models.DateTimeField('Fecha de realizacion de la cotizacion',blank=True,null=True, default=dateutil.utils.today())
    dispositivos = models.ManyToManyField(Dispositivo, blank = True)

    def save(self, *args, **kwargs):
        super(Cliente, self).save(*args, **kwargs)
        opciones = Dispositivo.objects.all()
        for opcion in opciones:
            self.dispositivos.add(opcion)
        super(Cliente, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']


class cotizacion_servicio(models.Model):
    num_list = [(1,"1"),(2,"2"),(4,"4"),(6,"6")]
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField(verbose_name="Nombre Cotizacion", null=True, blank=True)
    periodisidadxano = models.IntegerField(verbose_name="Periodicidad regular de actividad de mtto por año", choices=num_list, blank=True, null=True)
    periodoextra = models.BooleanField(verbose_name="¿Quieres Periodicidad Adicional a la regular?", default=False)


class Nombre_servicio(models.Model):
    titulo = models.CharField(
        max_length=200, verbose_name="Titulo Mantenimiento", null=True, blank=True)
    encargado = models.ForeignKey(Precio, on_delete=models.CASCADE, null=True)
    tiempodeejecucion = models.FloatField(
        verbose_name="Tiempo de Ejecucion", null=True)

    def __str__(self):
        return self.titulo

class Mantenimiento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    cotizacion = models.ForeignKey(cotizacion_servicio, on_delete=models.CASCADE, null=True, blank=True)
    result=[]
    for titulo in Nombre_servicio.objects.all():
        result.append((titulo.titulo,titulo.titulo))
    
    Titulo = models.CharField(max_length=200,choices=result,blank=True)
    periodisidadactividades = models.IntegerField(verbose_name="Periodicidad regular de actividad de mtto por año", blank=True, null=True )
    periodisidadadicional = models.FloatField(verbose_name="Periodicidad adicional de actividad de mtto  a la regular", blank=True, null=True)
    tiempoejecucion = models.FloatField(verbose_name="Tiempo de ejecucion del mtto", blank=True, null=True)
    cantidaddispositivos = models.IntegerField(verbose_name="Cantidad de dispositivos a considerar en periodicidad regular", blank=True, null=True)
    cantidaddispositivosextras = models.IntegerField(verbose_name="Cantidad de dispositivos a considerar en periodicidad Extra", blank=True, null=True)
    horasactividad = models.IntegerField(verbose_name="horas por actividad de mtto regular =Importe de cantidad x Tiempo de ejecucion", blank=True, null=True)
    costomantenimientoadicional = models.FloatField(verbose_name="Costo Adicional = horas por actividad de mtto adicional =Importe de cantidad x Tiempo de ejecucion ", blank=True, null=True)
    costomantenimientoregular = models.FloatField(verbose_name="Costo Regular = horas por actividad de mtto regular =Importe de cantidad x Tiempo de ejecucion",null=True,blank=True)

    encargadoTrabajo1 = models.ForeignKey(Precio,verbose_name="Encargado del trabajo" ,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
            # Para los titulos dentro de la base de datos Nombre_Servicio
            for titulo in Nombre_servicio.objects.all():
                # Se busca el titulo que sea equivalente al titulo en Nombre_Servicio
                if self.Titulo == titulo.titulo:
                    # se asigna las variables con las de la base de datos Nombre_Servicio
                    self.encargadoTrabajo1 = titulo.encargado
                    self.tiempoejecucion = titulo.tiempodeejecucion
                    # self.cantidaddispositivos = titulo.cantidaddedispositivos
                    # self.cantidaddispositivosextras = titulo.cantidaddedispositivosextra
                    # Se obtienen varioles finales con variables previamente asignadas por medio de multiplicaciones.
                    self.horasactividad = self.tiempoejecucion * self.cantidaddispositivos
                    self.costomantenimientoadicional = self.tiempoejecucion * self.cantidaddispositivosextras * self.periodisidadadicional
                    self.costomantenimientoadicional = self.costomantenimientoadicional * self.encargadoTrabajo1.precio
                    self.costomantenimientoregular = self.encargadoTrabajo1.precio * self.horasactividad
                    super(Mantenimiento, self).save(*args, **kwargs)
                    return
    def __str__(self):
        return self.Titulo

    class Meta:
        ordering = ['Titulo']
