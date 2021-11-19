# Generated by Django 3.2.8 on 2021-11-19 21:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RPA', '0053_informacionpersonal_puesto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotizacion',
            name='fecha',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 11, 19, 0, 0), null=True, verbose_name='Fecha de realizacion de la cotizacion'),
        ),
        migrations.AlterField(
            model_name='mantenimiento',
            name='cantidaddedispositivos',
            field=models.IntegerField(blank=True, null=True, verbose_name='Cantidad de dispositivos a considerar en periodicidad regular'),
        ),
        migrations.AlterField(
            model_name='mantenimiento',
            name='cantidaddispositivosextras',
            field=models.IntegerField(blank=True, null=True, verbose_name='Cantidad de dispositivos a considerar en periodicidad Extra'),
        ),
    ]