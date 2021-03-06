# Generated by Django 3.2.8 on 2021-10-26 17:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RPA', '0023_auto_20211025_1154'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nombre_servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(blank=True, max_length=200, null=True, verbose_name='Titulo Mantenimiento')),
            ],
        ),
        migrations.AlterField(
            model_name='cliente',
            name='fecha',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 10, 26, 0, 0), null=True, verbose_name='Fecha de realizacion de la cotizacion'),
        ),
    ]
