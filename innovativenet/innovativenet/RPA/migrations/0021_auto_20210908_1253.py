# Generated by Django 3.2.6 on 2021-09-08 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RPA', '0020_auto_20210908_1237'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='dispositivo',
        ),
        migrations.AddField(
            model_name='dispositivo',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='RPA.cliente'),
        ),
    ]
