# Generated by Django 4.0.3 on 2022-03-27 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_remove_concreteorder_f_items_flatworkitem_order_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gravelorder',
            name='ddate',
        ),
        migrations.RemoveField(
            model_name='historicalgravelorder',
            name='ddate',
        ),
    ]
