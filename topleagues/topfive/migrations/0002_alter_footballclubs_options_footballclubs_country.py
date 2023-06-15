# Generated by Django 4.2.1 on 2023-06-04 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topfive', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='footballclubs',
            options={'ordering': ['id'], 'verbose_name': 'Футбольный клуб', 'verbose_name_plural': 'Футбольные клубы'},
        ),
        migrations.AddField(
            model_name='footballclubs',
            name='country',
            field=models.CharField(max_length=255, null=True, verbose_name='страна'),
        ),
    ]
