# Generated by Django 3.2 on 2021-10-29 21:50

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RPA', '0028_auto_20211027_1203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nombre_servicio',
            name='cantidaddedispositivos',
        ),
        migrations.RemoveField(
            model_name='nombre_servicio',
            name='cantidaddedispositivosextra',
        ),
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 10, 29, 0, 0), null=True, verbose_name='Fecha de realizacion de la cotizacion'),
        ),
        migrations.AlterField(
            model_name='mantenimiento',
            name='Titulo',
            field=models.CharField(blank=True, choices=[('Revision y limpieza de panel de alarmas / Remoto', 'Revision y limpieza de panel de alarmas / Remoto'), ('Revisión y limpieza de sensores de humo', 'Revisión y limpieza de sensores de humo'), ('Revisión y limpieza de estrobos -cornetas - campanas-mixtos', 'Revisión y limpieza de estrobos -cornetas - campanas-mixtos'), ('Revisión y limpieza de Fuentes de poder', 'Revisión y limpieza de Fuentes de poder'), ('Revisión y limpieza Palancas  de activación', 'Revisión y limpieza Palancas  de activación'), ('Revisión y limpieza Módulos monitores de Flujo', 'Revisión y limpieza Módulos monitores de Flujo'), ('Revisión y limpieza sensores de ductos de aire', 'Revisión y limpieza sensores de ductos de aire'), ('Revisión y limpieza Sensor de humo tipo Beam', 'Revisión y limpieza Sensor de humo tipo Beam'), ('Revisión y limpieza de módulos de Control', 'Revisión y limpieza de módulos de Control'), ('Revisión y limpieza de modulo de control CT1 o CT2', 'Revisión y limpieza de modulo de control CT1 o CT2'), ('Revisión y limpieza de modulo relevador CR', 'Revisión y limpieza de modulo relevador CR'), ('Revisión y Verificación de resistencias de fin de línea', 'Revisión y Verificación de resistencias de fin de línea'), ('Cambiar ubicaciones Herramientas y personal (mover el punto A al punto B)', 'Cambiar ubicaciones Herramientas y personal (mover el punto A al punto B)'), ('Relleno de informe', 'Relleno de informe'), ('Prueba de comunicación de datos entre panel y dispositivos, así como los loops.', 'Prueba de comunicación de datos entre panel y dispositivos, así como los loops.'), ('Servicio de soporte técnico -Horas de servicios generales adicionales', 'Servicio de soporte técnico -Horas de servicios generales adicionales')], max_length=200),
        ),
        migrations.AlterField(
            model_name='mantenimiento',
            name='cantidaddispositivosextras',
            field=models.IntegerField(blank=True, null=True, verbose_name='Cantidad de dispositivos a considerar en periodicidad Extra'),
        ),
        migrations.AlterField(
            model_name='mantenimiento',
            name='periodisidadadicional',
            field=models.FloatField(blank=True, null=True, verbose_name='Periodicidad adicional de actividad de mtto  a la regular'),
        ),
        migrations.AlterField(
            model_name='mantenimiento',
            name='tiempoejecucion',
            field=models.FloatField(blank=True, null=True, verbose_name='Tiempo de ejecucion del mtto'),
        ),
        migrations.AlterField(
            model_name='precio',
            name='precio',
            field=models.FloatField(blank=True, null=True, verbose_name='Precio por hora'),
        ),
        migrations.CreateModel(
            name='cotizacion_servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombre Cotizacion')),
                ('periodisidadxano', models.IntegerField(blank=True, choices=[(1, '1'), (2, '2'), (4, '4'), (6, '6')], null=True, verbose_name='Periodicidad regular de actividad de mtto por año')),
                ('periodoextra', models.BooleanField(default=False, verbose_name='¿Quieres Periodicidad Adicional a la regular?')),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='RPA.cliente')),
            ],
        ),
        migrations.AddField(
            model_name='mantenimiento',
            name='cotizacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='RPA.cotizacion_servicio'),
        ),
    ]
