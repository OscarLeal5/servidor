# Generated by Django 3.2.8 on 2021-11-01 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RPA', '0035_alter_cotizacion_mantenimiento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotizacion',
            name='Mantenimiento',
            field=models.ManyToManyField(through='RPA.Mantenimiento', to='RPA.nombre_servicio'),
        ),
    ]
