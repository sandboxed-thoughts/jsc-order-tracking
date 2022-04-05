# Generated by Django 4.0.3 on 2022-04-05 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_historicalnotemodel_note_alter_notemodel_note'),
        ('orders', '0013_remove_historicalinspectionmodel_order_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GravelOrderNote',
            fields=[
                ('notemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.notemodel')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gravel_orders', to='orders.gravelorder', verbose_name='gravel order')),
            ],
            options={
                'verbose_name': 'order note',
                'verbose_name_plural': 'order notes',
                'db_table': 'orders_gravel_order_notes',
                'managed': True,
            },
            bases=('core.notemodel',),
        ),
    ]
