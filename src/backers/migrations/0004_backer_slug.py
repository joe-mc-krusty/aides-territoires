# Generated by Django 2.2.9 on 2020-04-21 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backers', '0003_backer_is_corporate'),
    ]

    operations = [
        migrations.AddField(
            model_name='backer',
            name='slug',
            field=models.SlugField(default='', verbose_name='Slug'),
            preserve_default=False,
        ),
    ]