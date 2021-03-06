# Generated by Django 3.2.5 on 2021-09-06 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RPA', '0015_auto_20210906_1030'),
    ]

    operations = [
        migrations.CreateModel(
            name='Precio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('encargado', models.CharField(blank=True, max_length=50, null=True, verbose_name='Encargado del trabajo')),
                ('precio', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Precio por hora')),
            ],
            options={
                'ordering': ['encargado'],
            },
        ),
    ]
