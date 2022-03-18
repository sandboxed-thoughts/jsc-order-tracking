# Generated by Django 4.0.3 on 2022-03-18 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='builder',
            name='subdivisions',
            field=models.ManyToManyField(related_name='builders', through='clients.Lot', to='clients.subdivision', verbose_name='subdivisions'),
        ),
    ]
