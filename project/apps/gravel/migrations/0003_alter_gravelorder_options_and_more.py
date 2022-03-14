# Generated by Django 4.0.3 on 2022-03-13 05:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('gravel', '0002_alter_graveldelivery_sdate'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gravelorder',
            options={'managed': True, 'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='historicalgravelorder',
            options={'get_latest_by': 'history_date', 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Order'},
        ),
        migrations.AlterField(
            model_name='graveldelivery',
            name='sdate',
            field=models.DateField(default=datetime.datetime(2022, 3, 13, 5, 40, 46, 151033, tzinfo=utc), verbose_name='scheduled on'),
        ),
        migrations.AlterModelTable(
            name='gravelorder',
            table='orders_gravel',
        ),
    ]