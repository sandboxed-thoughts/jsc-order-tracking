# Generated by Django 4.0.3 on 2022-03-16 13:30

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('suppliers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GravelOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('po', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('[\\S\\w]')], verbose_name='Purchase Order')),
                ('priority', models.CharField(max_length=50, verbose_name='priority')),
                ('bsdt', models.CharField(blank=True, max_length=50, null=True, verbose_name='B/S D/T')),
                ('need_by', models.DateField(verbose_name='date needed')),
                ('rloads', models.SmallIntegerField(verbose_name='loads requested')),
                ('dloads', models.SmallIntegerField(default=0, verbose_name='loads delivered')),
                ('ddate', models.DateField(blank=True, null=True, verbose_name='date delivered')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='suppliers.stonetype', verbose_name='stone type')),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clients.lot', verbose_name='lot')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='suppliers.supplier', verbose_name='supplier')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'db_table': 'orders_gravel',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='HistoricalGravelOrder',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('po', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('[\\S\\w]')], verbose_name='Purchase Order')),
                ('priority', models.CharField(max_length=50, verbose_name='priority')),
                ('bsdt', models.CharField(blank=True, max_length=50, null=True, verbose_name='B/S D/T')),
                ('need_by', models.DateField(verbose_name='date needed')),
                ('rloads', models.SmallIntegerField(verbose_name='loads requested')),
                ('dloads', models.SmallIntegerField(default=0, verbose_name='loads delivered')),
                ('ddate', models.DateField(blank=True, null=True, verbose_name='date delivered')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='suppliers.stonetype', verbose_name='stone type')),
                ('lot', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='clients.lot', verbose_name='lot')),
                ('supplier', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='suppliers.supplier', verbose_name='supplier')),
            ],
            options={
                'verbose_name': 'historical Order',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalGravelDelivery',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('sdate', models.DateField(default=django.utils.timezone.now, verbose_name='scheduled for')),
                ('loads', models.SmallIntegerField(default=1, verbose_name='loads')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='notes')),
                ('status', models.CharField(choices=[('scheduled', 'scheduled'), ('in progress', 'in progress'), ('complete', 'complete')], default='scheduled', max_length=11, verbose_name='status')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('ddriver', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='delivery driver')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='gravel.gravelorder', verbose_name='order')),
            ],
            options={
                'verbose_name': 'historical Gravel Delivery',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='GravelDelivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sdate', models.DateField(default=django.utils.timezone.now, verbose_name='scheduled for')),
                ('loads', models.SmallIntegerField(default=1, verbose_name='loads')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='notes')),
                ('status', models.CharField(choices=[('scheduled', 'scheduled'), ('in progress', 'in progress'), ('complete', 'complete')], default='scheduled', max_length=11, verbose_name='status')),
                ('ddriver', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='deliveries', to=settings.AUTH_USER_MODEL, verbose_name='delivery driver')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gravel.gravelorder', verbose_name='order')),
            ],
            options={
                'verbose_name': 'Gravel Delivery',
                'verbose_name_plural': 'Gravel Deliveries',
                'db_table': 'orders_gravel_deliveries',
                'managed': True,
            },
        ),
    ]
