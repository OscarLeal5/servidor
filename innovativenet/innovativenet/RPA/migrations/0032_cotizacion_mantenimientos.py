# Generated by Django 3.2.8 on 2021-11-01 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RPA', '0031_auto_20211101_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='cotizacion',
            name='Mantenimientos',
            field=models.ManyToManyField(through='RPA.Mantenimiento', to='RPA.Nombre_servicio'),
        ),
    ]