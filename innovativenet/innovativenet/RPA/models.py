from django.db import models
from django.contrib.auth.models import User
import dateutil.utils

class Precio(models.Model):
    encargado = models.CharField(max_length=50, verbose_name='Encargado del trabajo',blank=True, null=True)
    precio = models.DecimalField("Precio por hora",max_digits=5,decimal_places=2,blank=True, null=True)

    def __str__(self):
        return self.encargado
    class Meta:
        ordering = ['encargado']


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

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']

class Dispositivo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    marca = models.CharField(max_length=200, verbose_name="Marca del dispositivo", null=True, blank=True)
    titulo = models.CharField(max_length=200, verbose_name="Nombre del dispositivo", null=True, blank=True)
    cantidad = models.IntegerField(verbose_name="Cantidad de dispositivos actuales", null=True)
    actividad = models.CharField(max_length=200, verbose_name="Actividad de mantenimiento a realizar",null=True, blank=True)
    plan = models.CharField(max_length=200, verbose_name="Tipo de poliza/plan", null=True, blank=True)

    def __str__(self):
        return self.marca +" "+ self.titulo
    class Meta:
        ordering = ['titulo']
        
class Mantenimiento(models.Model):
    #title = models.CharField(max_length=200, verbose_name="Titulo Mantenimiento", null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    limpieza_panel_alarmas = 'Revision y limpieza de panel de alarmas / Remoto'
    revision_limpieza_sensor_humo = 'Revision y limpieza de sensores de humo'
    rev_limp_estrobos = ' Revision y limpieza de estrobos -cornetas - campanas-mixtos'
    rev_limp_fuentespoder = 'Revision y limpieza de Fuentes de poder'
    rev_limp_placasactivacion = 'Revision y limpieza Palancas  de activacion'
    rev_limp_monitoresflujo = 'Revision y limpieza Modulos monitores de Flujo'
    rev_limp_sensoresductos = 'Revision y limpieza sensores de ductos de aire'
    rev_limp_humobeam = 'Revision y limpieza Sensor de humo tipo Beam'
    rev_limp_modulodecontrol = 'Revision y limpieza de modulos de Control'
    rev_limp_modconttrct1ct2 = 'Revision y limpieza de modulo de control CT1 o CT2'
    rev_limp_modreleevadorcr = 'Revision y limpieza de modulo releevador CR'
    rev_veri_resistenciafinlinea = 'Revision y Verificacion de resistencias de fin de linea'
    cambiar_ubi_herramientrasypersonal = 'Cambiar ubicaciones Herramientas y personal (mover el punto A al punto B)'
    relleno_informe = 'Relleno de informe'
    prueba_com_datospanelydisp = 'Prueba de comunicación de datos entre panel y dispositivos, asi como los loops.'
    soporte_tecnico = 'Servicio de soporte técnico -Horas de servicios generales adicionales'

    MANTENIMIENTOS_LISTA = [
        (limpieza_panel_alarmas, 'Revision y limpieza de panel de alarmas / Remoto'),
        (revision_limpieza_sensor_humo, 'Revision y limpieza de sensores de humo'),
        (rev_limp_estrobos, 'Revision y limpieza de estrobos -cornetas - campanas-mixtos'),
        (rev_limp_fuentespoder, 'Revision y limpieza de Fuentes de poder'),
        (rev_limp_placasactivacion, 'Revision y limpieza Palancas  de activacion'),
        (rev_limp_monitoresflujo, 'Revision y limpieza Modulos monitores de Flujo'),
        (rev_limp_sensoresductos, 'Revision y limpieza sensores de ductos de aire'),
        (rev_limp_humobeam, 'Revision y limpieza Sensor de humo tipo Beam'),
        (rev_limp_modulodecontrol, 'Revision y limpieza de modulos de Control'),
        (rev_limp_modconttrct1ct2, 'Revision y limpieza de modulo de control CT1 o CT2'),
        (rev_limp_modreleevadorcr, 'Revision y limpieza de modulo releevador CR'),
        (rev_veri_resistenciafinlinea,'Revision y Verificacion de resistencias de fin de linea'),
        (cambiar_ubi_herramientrasypersonal,'Cambiar ubicaciones Herramientas y personal (mover el punto A al punto B)'),
        (relleno_informe,'Relleno de informe'),
        (prueba_com_datospanelydisp, 'Prueba de comunicación de datos entre panel y dispositivos, asi como los loops.'),
        (soporte_tecnico, 'Servicio de soporte técnico -Horas de servicios generales adicionales'),
    ]
    Titulo = models.CharField(
        max_length=200,
        choices=MANTENIMIENTOS_LISTA,
        blank=True
    )
    periodisidadactividades = models.IntegerField(verbose_name="Periodicidad regular de actividad de mtto por año", blank=True, null=True )
    periodisidadadicional = models.IntegerField(verbose_name="Periodicidad adicional de actividad de mtto  a la regular", blank=True, null=True)
    tiempoejecucion = models.IntegerField(verbose_name="Tiempo de ejecucion del mtto", blank=True, null=True)
    cantidaddispositivos = models.IntegerField(verbose_name="Cantidad de dispositivos a considerar en periodicidad regular", blank=True, null=True)
    horasactividad = models.IntegerField(verbose_name="horas por actividad de mtto regular =Importe de cantidad x Tiempo de ejecucion", blank=True, null=True)
    costomantenimientoadicional = models.FloatField(verbose_name="Costo Adicional = horas por actividad de mtto adicional =Importe de cantidad x Tiempo de ejecucion ", blank=True, null=True)
    costomantenimientoregular = models.FloatField(verbose_name="Costo Regular = horas por actividad de mtto regular =Importe de cantidad x Tiempo de ejecucion",null=True,blank=True)

    encargadoTrabajo1 = models.ForeignKey(Precio,verbose_name="Encargado del trabajo" ,on_delete=models.CASCADE)


    def save(self, *args, **kwargs):
            if self.Titulo == self.relleno_informe:
                self.encargadoTrabajo1 = Precio.objects.get(encargado='Ingeniero')
            elif self.Titulo == self.prueba_com_datospanelydisp:
                self.encargadoTrabajo1 = Precio.objects.get(encargado='Ingeniero')
            elif self.Titulo == self.soporte_tecnico:
                self.encargadoTrabajo1 = Precio.objects.get(encargado='Ingeniero')
            else:
                self.encargadoTrabajo1 = Precio.objects.get(encargado='Equipo de Tecnicos')
            self.costomantenimientoregular = self.encargadoTrabajo1.precio * self.horasactividad
            super(Mantenimiento, self).save(*args, **kwargs)

    def __str__(self):
        return self.Titulo

    class Meta:
        ordering = ['Titulo']