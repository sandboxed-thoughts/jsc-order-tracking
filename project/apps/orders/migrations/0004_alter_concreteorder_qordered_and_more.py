# Generated by Django 4.0.4 on 2022-04-14 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_concreteorder_historicalconcreteordernote_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concreteorder',
            name='qordered',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='total ordered'),
        ),
        migrations.AlterField(
            model_name='historicalconcreteorder',
            name='qordered',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='total ordered'),
        ),
    ]
