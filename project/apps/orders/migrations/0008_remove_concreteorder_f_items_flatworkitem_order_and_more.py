# Generated by Django 4.0.3 on 2022-03-26 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_footingsitem_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='concreteorder',
            name='f_items',
        ),
        migrations.AddField(
            model_name='flatworkitem',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='orders.concreteorder', verbose_name='order'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='FlatworkOrderItems',
        ),
    ]