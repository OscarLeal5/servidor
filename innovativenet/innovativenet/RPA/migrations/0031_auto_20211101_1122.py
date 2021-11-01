# Generated by Django 3.2.8 on 2021-11-01 18:22

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RPA', '0030_merge_0029_auto_20211029_1450_0029_auto_20211101_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mantenimiento',
            name='Titulo',
            field=models.CharField(blank=True, choices=[], max_length=200),
        ),
        migrations.CreateModel(
            name='Cotizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombre Cotizacion')),
                ('lugar_de_mantenimiento', models.CharField(blank=True, max_length=120, verbose_name='Lugar en que se realizara el mantenimiento')),
                ('descripcion_cotizacion', models.TextField(blank=True, verbose_name='Descripcion de la cotizacion')),
                ('fecha', models.DateTimeField(blank=True, default=datetime.datetime(2021, 11, 1, 0, 0), null=True, verbose_name='Fecha de realizacion de la cotizacion')),
                ('periodisidadxano', models.IntegerField(blank=True, choices=[(1, '1'), (2, '2'), (4, '4'), (6, '6')], null=True, verbose_name='Periodicidad regular de actividad de mtto por año')),
                ('periodoextra', models.BooleanField(default=False, verbose_name='¿Quieres Periodicidad Adicional a la regular?')),
                ('Mantenimiento', models.ManyToManyField(through='RPA.Mantenimiento', to='RPA.nombre_servicio')),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='RPA.cliente')),
            ],
            options={
                'ordering': ['titulo'],
            },
        ),
    ]
