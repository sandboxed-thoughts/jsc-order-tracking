# Generated by Django 4.0.3 on 2022-03-29 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concrete', '0003_alter_concretetype_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concretetype',
            name='note',
            field=models.TextField(blank=True, max_length=250, null=True, verbose_name='note'),
        ),
    ]
