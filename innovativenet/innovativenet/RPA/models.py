from django.db import models
from django.contrib.auth.models import User

class Mantenimiento(models.Model):
    #title = models.CharField(max_length=200, verbose_name="Titulo Mantenimiento", null=True, blank=True)
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
    costomantenimientoregular = models.FloatField(verbose_name="Costo Regular = horas por actividad de mtto regular =Importe de cantidad x Tiempo de ejecucion",null=True)

    Tecnico = 'Tecnico'
    precioTecnico = 23.68
    ProjectManager = 'Project Manager'
    precioProject = 78.95
    Engineering = 'Ingeniero'
    precioEngineering = 71.05
    Team = 'Equipo de tecnicos'
    precioTeam = 47.36
    Electrical = 'Electrico'
    precioElectrical = 23.68
    Trainer = 'Trainer'
    precioTrainer = 78.95
    tipoDeTrabajo=[(Tecnico,'Tecnico'),
                   (ProjectManager,'Project Manager'),
                   (Engineering,'Ingeniero'),
                   (Team,'Equipo de Tecnicos'),
                   (Electrical,'Electrico'),
                   (Trainer,'Trainer'),
                   ]

    encargadoTrabajo = models.CharField(max_length=30,choices=tipoDeTrabajo,default=Tecnico)

    # if encargadoTrabajo =='Tecnico':
    #     costomantenimientoregular = precioTecnico * horasactividad
    #     Mantenimiento.save()
    # elif encargadoTrabajo == 'Trainer':
    #     costomantenimientoregular = precioTrainer * horasactividad
    # elif encargadoTrabajo == 'Electrico':
    #     costomantenimientoregular = precioElectrical * horasactividad
    # elif encargadoTrabajo == 'Equipo de tecnicos':
    #     costomantenimientoregular = precioTeam * horasactividad
    # elif encargadoTrabajo == 'Ingeniero':
    #     costomantenimientoregular = precioEngineering * horasactividad
    # elif encargadoTrabajo == 'Project Manager':
    #     costomantenimientoregular = precioProject * horasactividad

    def update_costo(self):
        if self.encargadoTrabajo == 'Tecnico':
            self.costomantenimientoregular = self.precioTecnico * self.horasactividad
            Mantenimiento.save(self)
        elif self.encargadoTrabajo == 'Trainer':
            self.costomantenimientoregular = self.precioTrainer * self.horasactividad
            Mantenimiento.save(self)
        elif self.encargadoTrabajo == 'Electrico':
            self.costomantenimientoregular = self.precioElectrical * self.horasactividad
            Mantenimiento.save(self)
        elif self.encargadoTrabajo == 'Equipo de tecnicos':
            self.costomantenimientoregular = self.precioTeam * self.horasactividad
            Mantenimiento.save(self)
        elif self.encargadoTrabajo == 'Ingeniero':
            self.costomantenimientoregular = self.precioEngineering * self.horasactividad
            Mantenimiento.save(self)
        elif self.encargadoTrabajo == 'Project Manager':
            self.costomantenimientoregular = self.precioProject * self.horasactividad
            Mantenimiento.save(self)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Dispositivo(models.Model):
    marca = models.CharField(max_length=200, verbose_name="Marca del dispositivo", null=True, blank=True)
    titulo = models.CharField(max_length=200, verbose_name="Nombre del dispositivo", null=True, blank=True)
    cantidad = models.IntegerField(verbose_name="Cantidad de dispositivos actuales", null=True)
    actividad = models.CharField(max_length=200, verbose_name="Actividad de mantenimiento a realizar",null=True, blank=True)
    plan = models.CharField(max_length=200, verbose_name="Tipo de poliza/plan", null=True, blank=True)

    def __str__(self):
        return self.marca +" "+ self.titulo
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
    fecha = models.DateTimeField('Fecha de realizacion de la cotizacion',blank=True,null=True)

    mantenimiento = models.ManyToManyField(Mantenimiento, blank=True, related_name='cliente')
    dispositivo = models.ManyToManyField(Dispositivo, blank=True, related_name="cliente")

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']