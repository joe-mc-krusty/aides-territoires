# Generated by Django 2.1 on 2018-08-28 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aids', '0010_auto_20180816_1204'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aid',
            name='diffusion_perimeter',
        ),
        migrations.RemoveField(
            model_name='aid',
            name='diffusion_perimeter_detail',
        ),
    ]
