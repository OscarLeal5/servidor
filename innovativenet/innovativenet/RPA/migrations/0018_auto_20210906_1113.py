# Generated by Django 3.2.5 on 2021-09-06 18:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RPA', '0017_auto_20210906_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 9, 6, 0, 0), null=True, verbose_name='Fecha de realizacion de la cotizacion'),
        ),
        migrations.AlterField(
            model_name='mantenimiento',
            name='costomantenimientoregular',
            field=models.FloatField(blank=True, null=True, verbose_name='Costo Regular = horas por actividad de mtto regular =Importe de cantidad x Tiempo de ejecucion'),
        ),
    ]
