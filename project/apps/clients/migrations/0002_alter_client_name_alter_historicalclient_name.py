# Generated by Django 4.0.4 on 2022-04-15 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(max_length=150, unique=True, verbose_name='builder name'),
        ),
        migrations.AlterField(
            model_name='historicalclient',
            name='name',
            field=models.CharField(db_index=True, max_length=150, verbose_name='builder name'),
        ),
    ]