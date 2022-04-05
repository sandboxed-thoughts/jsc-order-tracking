# Generated by Django 4.0.3 on 2022-04-05 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_alter_historicalinspectionmodel_note_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalinspectionmodel',
            name='order',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='orders.concreteorder', verbose_name='concrete order'),
        ),
        migrations.AddField(
            model_name='inspectionmodel',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='orders.concreteorder', verbose_name='concrete order'),
            preserve_default=False,
        ),
    ]
