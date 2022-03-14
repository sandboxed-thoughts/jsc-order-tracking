# Generated by Django 4.0.3 on 2022-03-13 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gravel', '0006_graveldelivery_notes_historicalgraveldelivery_notes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='graveldelivery',
            name='status',
            field=models.CharField(choices=[('scheduled', 'scheduled'), ('in progress', 'in progress'), ('complete', 'complete')], default='scheduled', max_length=11, verbose_name='status'),
        ),
        migrations.AddField(
            model_name='historicalgraveldelivery',
            name='status',
            field=models.CharField(choices=[('scheduled', 'scheduled'), ('in progress', 'in progress'), ('complete', 'complete')], default='scheduled', max_length=11, verbose_name='status'),
        ),
    ]