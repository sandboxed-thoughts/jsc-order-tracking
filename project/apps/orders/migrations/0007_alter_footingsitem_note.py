# Generated by Django 4.0.3 on 2022-03-26 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_remove_concreteordernote_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footingsitem',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='note'),
        ),
    ]