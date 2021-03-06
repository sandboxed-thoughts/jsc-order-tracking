# Generated by Django 4.0.4 on 2022-04-13 21:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0001_initial'),
        ('supplies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GravelOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.CharField(blank=True, max_length=50, null=True, verbose_name='priority')),
                ('lots', models.CharField(help_text='separate lots with a comma. Example: "1547 Cherrywood St, 1549 Cherrywood St, 2867 Flintwood Cir', max_length=150, verbose_name='lots')),
                ('bsdt', models.CharField(choices=[('b/s', 'b/s'), ('d/t', 'd/t')], max_length=3, verbose_name='B/S D/T')),
                ('po', models.CharField(blank=True, max_length=150, null=True, validators=[django.core.validators.RegexValidator('[[\\S\\w]')], verbose_name='purchase order')),
                ('need_by', models.DateField(blank=True, null=True, verbose_name='date needed')),
                ('rloads', models.SmallIntegerField(blank=True, null=True, verbose_name='loads requested')),
                ('dloads', models.SmallIntegerField(default=0, verbose_name='loads delivered')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('placed', 'Placed'), ('canceled', 'canceled'), ('completed', 'completed')], default='pending', max_length=10, verbose_name='status')),
                ('builder', models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.PROTECT, related_name='builder_gravel_orders', to='clients.client', verbose_name='builder')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='gravel_order_items', to='supplies.gravelitem', verbose_name='item')),
                ('site', models.ForeignKey(blank=True, limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='site_gravel_deliveries', to='clients.site', verbose_name='site')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='supplies.supplier', verbose_name='supplier')),
            ],
            options={
                'verbose_name': 'gravel order',
                'verbose_name_plural': 'gravel orders',
                'db_table': 'orders_gravel',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='HistoricalGravelOrderNote',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('note', models.TextField(max_length=250, verbose_name='Note')),
                ('created_on', models.DateTimeField(blank=True, editable=False)),
                ('updated_on', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('author', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='submitted by')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='orders.gravelorder', verbose_name='gravel order')),
            ],
            options={
                'verbose_name': 'historical order note',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalGravelOrder',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('priority', models.CharField(blank=True, max_length=50, null=True, verbose_name='priority')),
                ('lots', models.CharField(help_text='separate lots with a comma. Example: "1547 Cherrywood St, 1549 Cherrywood St, 2867 Flintwood Cir', max_length=150, verbose_name='lots')),
                ('bsdt', models.CharField(choices=[('b/s', 'b/s'), ('d/t', 'd/t')], max_length=3, verbose_name='B/S D/T')),
                ('po', models.CharField(blank=True, max_length=150, null=True, validators=[django.core.validators.RegexValidator('[[\\S\\w]')], verbose_name='purchase order')),
                ('need_by', models.DateField(blank=True, null=True, verbose_name='date needed')),
                ('rloads', models.SmallIntegerField(blank=True, null=True, verbose_name='loads requested')),
                ('dloads', models.SmallIntegerField(default=0, verbose_name='loads delivered')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('placed', 'Placed'), ('canceled', 'canceled'), ('completed', 'completed')], default='pending', max_length=10, verbose_name='status')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('builder', models.ForeignKey(blank=True, db_constraint=False, limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='clients.client', verbose_name='builder')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='supplies.gravelitem', verbose_name='item')),
                ('site', models.ForeignKey(blank=True, db_constraint=False, limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='clients.site', verbose_name='site')),
                ('supplier', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='supplies.supplier', verbose_name='supplier')),
            ],
            options={
                'verbose_name': 'historical gravel order',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='GravelOrderNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(max_length=250, verbose_name='Note')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='submitted by')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gravel_order_notes', to='orders.gravelorder', verbose_name='gravel order')),
            ],
            options={
                'verbose_name': 'order note',
                'verbose_name_plural': 'order notes',
                'db_table': 'orders_gravel_order_notes',
                'managed': True,
            },
        ),
    ]
