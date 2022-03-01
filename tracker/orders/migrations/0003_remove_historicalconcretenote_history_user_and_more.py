# Generated by Django 4.0.2 on 2022-03-01 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_concrete_pinfo_alter_historicalconcrete_pinfo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalconcretenote',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalconcretenote',
            name='order',
        ),
        migrations.AddField(
            model_name='concrete',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='order notes'),
        ),
        migrations.AddField(
            model_name='historicalconcrete',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='order notes'),
        ),
        migrations.AlterField(
            model_name='gravel',
            name='bsdt',
            field=models.CharField(choices=[('B', 'B/S'), ('D', 'D/T')], default='B', max_length=2, verbose_name='B/S D/T'),
        ),
        migrations.AlterField(
            model_name='historicalgravel',
            name='bsdt',
            field=models.CharField(choices=[('B', 'B/S'), ('D', 'D/T')], default='B', max_length=2, verbose_name='B/S D/T'),
        ),
        migrations.DeleteModel(
            name='ConcreteNote',
        ),
        migrations.DeleteModel(
            name='HistoricalConcreteNote',
        ),
    ]
