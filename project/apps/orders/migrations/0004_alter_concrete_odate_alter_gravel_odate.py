# Generated by Django 4.0.3 on 2022-03-09 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_gravel_d_date_remove_gravel_n_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concrete',
            name='odate',
            field=models.DateField(auto_now_add=True, verbose_name='Date Ordered'),
        ),
        migrations.AlterField(
            model_name='gravel',
            name='odate',
            field=models.DateField(auto_now_add=True, verbose_name='Date Ordered'),
        ),
    ]
