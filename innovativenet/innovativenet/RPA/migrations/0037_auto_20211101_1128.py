# Generated by Django 3.2.8 on 2021-11-01 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RPA', '0036_alter_cotizacion_mantenimiento'),
    ]

    operations = [
        migrations.AddField(
            model_name='mantenimiento',
            name='cotizacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='RPA.cotizacion'),
        ),
        migrations.AlterField(
            model_name='cotizacion',
            name='Mantenimiento',
            field=models.ManyToManyField(through='RPA.Mantenimiento', to='RPA.nombre_servicio'),
        ),
    ]
