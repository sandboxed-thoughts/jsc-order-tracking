# Generated by Django 4.0.3 on 2022-04-05 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0012_merge_20220328_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pumpschedulenote',
            name='pump',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pump_schedule_notes', to='schedules.pumpschedule', verbose_name='pump'),
        ),
    ]
