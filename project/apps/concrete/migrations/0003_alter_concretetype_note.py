# Generated by Django 4.0.3 on 2022-03-27 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concrete', '0002_concretetype_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concretetype',
            name='note',
            field=models.TextField(blank=True, null=True, verbose_name='note'),
        ),
    ]