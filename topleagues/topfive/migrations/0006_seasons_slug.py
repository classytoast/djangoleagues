# Generated by Django 4.2.1 on 2023-06-13 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topfive', '0005_countryleagues_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='seasons',
            name='slug',
            field=models.SlugField(max_length=255, null=True, unique=True, verbose_name='URL'),
        ),
    ]
