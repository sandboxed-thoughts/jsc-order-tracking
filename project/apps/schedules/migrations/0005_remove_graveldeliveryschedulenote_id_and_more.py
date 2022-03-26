# Generated by Django 4.0.3 on 2022-03-26 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_notemodel_options'),
        ('schedules', '0004_pumpschedulenote_graveldeliveryschedulenote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='graveldeliveryschedulenote',
            name='id',
        ),
        migrations.RemoveField(
            model_name='graveldeliveryschedulenote',
            name='note',
        ),
        migrations.RemoveField(
            model_name='pumpschedulenote',
            name='id',
        ),
        migrations.RemoveField(
            model_name='pumpschedulenote',
            name='note',
        ),
        migrations.AddField(
            model_name='graveldeliveryschedulenote',
            name='notemodel_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.notemodel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pumpschedulenote',
            name='notemodel_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.notemodel'),
            preserve_default=False,
        ),
    ]
