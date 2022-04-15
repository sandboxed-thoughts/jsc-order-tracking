# Generated by Django 4.0.4 on 2022-04-15 20:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0007_concreteorder_needs_pump_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConcreteOrderSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_delivers', models.BooleanField(default=False, help_text='Check if the supplier is responsible for delivering the order', verbose_name='supplier delivers')),
                ('crew', models.CharField(blank=True, max_length=150, null=True, verbose_name='crew pouring')),
                ('pdate', models.DateField(blank=True, null=True, verbose_name='pour date')),
                ('ctime', models.TimeField(blank=True, null=True, verbose_name='concrete time')),
                ('loads', models.FloatField(default=0, verbose_name='loads')),
                ('progress', models.CharField(choices=[('will call', 'will call'), ('scheduled', 'scheduled'), ('canceled', 'canceled'), ('in_progress', 'in_progress'), ('released', 'released'), ('complete', 'complete')], default='will call', max_length=11, verbose_name='pump progress')),
                ('driver', models.ForeignKey(blank=True, limit_choices_to={'groups__name': 'Drivers'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='pump_schedules', to=settings.AUTH_USER_MODEL, verbose_name='delivery driver')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pump_schedule', to='orders.concreteorder', verbose_name='concrete order')),
            ],
            options={
                'verbose_name': 'pump',
                'db_table': 'concrete_pump_schedule',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='GravelDeliverySchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_delivers', models.BooleanField(default=False, help_text='Check if the supplier is responsible for delivering the order', verbose_name='supplier delivers')),
                ('sdate', models.DateField(default=django.utils.timezone.now, verbose_name='scheduled for')),
                ('loads', models.SmallIntegerField(default=1, verbose_name='loads')),
                ('status', models.CharField(choices=[('scheduled', 'scheduled'), ('in progress', 'in progress'), ('complete', 'complete')], default='scheduled', max_length=11, verbose_name='status')),
                ('ddate', models.DateTimeField(blank=True, null=True, verbose_name='delivered on')),
                ('driver', models.ForeignKey(blank=True, limit_choices_to={'groups__name': 'Drivers'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='deliveries', to=settings.AUTH_USER_MODEL, verbose_name='delivery driver')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='gravel_deliveries', to='orders.gravelorder', verbose_name='order')),
            ],
            options={
                'verbose_name': 'Gravel Delivery',
                'verbose_name_plural': 'Gravel Deliveries',
                'db_table': 'orders_gravel_deliveries',
                'ordering': ['-sdate', 'driver'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='InclimateWeather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp', models.CharField(max_length=50, verbose_name='temperature')),
                ('precip', models.CharField(max_length=50, verbose_name='precipitation')),
                ('pump', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pump_delay', to='schedules.concreteorderschedule', verbose_name='pump schedule')),
            ],
            options={
                'verbose_name': 'inclimate weather report',
                'verbose_name_plural': 'inclimate weather reports',
                'db_table': 'schedules_concrete_schedule_weather',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='InclimateWeatherNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(max_length=250, verbose_name='Note')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='submitted by')),
                ('delay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedules.inclimateweather', verbose_name='delay')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HistoricalInclimateWeatherNote',
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
                ('delay', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='schedules.inclimateweather', verbose_name='delay')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical inclimate weather note',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalInclimateWeather',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('temp', models.CharField(max_length=50, verbose_name='temperature')),
                ('precip', models.CharField(max_length=50, verbose_name='precipitation')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('pump', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='schedules.concreteorderschedule', verbose_name='pump schedule')),
            ],
            options={
                'verbose_name': 'historical inclimate weather report',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalGravelDeliveryScheduleNote',
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
                ('delivery', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='schedules.graveldeliveryschedule', verbose_name='pump')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Gravel Delivery Note',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalGravelDeliverySchedule',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('supplier_delivers', models.BooleanField(default=False, help_text='Check if the supplier is responsible for delivering the order', verbose_name='supplier delivers')),
                ('sdate', models.DateField(default=django.utils.timezone.now, verbose_name='scheduled for')),
                ('loads', models.SmallIntegerField(default=1, verbose_name='loads')),
                ('status', models.CharField(choices=[('scheduled', 'scheduled'), ('in progress', 'in progress'), ('complete', 'complete')], default='scheduled', max_length=11, verbose_name='status')),
                ('ddate', models.DateTimeField(blank=True, null=True, verbose_name='delivered on')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('driver', models.ForeignKey(blank=True, db_constraint=False, limit_choices_to={'groups__name': 'Drivers'}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='delivery driver')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='orders.gravelorder', verbose_name='order')),
            ],
            options={
                'verbose_name': 'historical Gravel Delivery',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalConcreteOrderScheduleNote',
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
                ('pump', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='schedules.concreteorderschedule', verbose_name='pump')),
            ],
            options={
                'verbose_name': 'historical Pump Schedule Note',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalConcreteOrderSchedule',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('supplier_delivers', models.BooleanField(default=False, help_text='Check if the supplier is responsible for delivering the order', verbose_name='supplier delivers')),
                ('crew', models.CharField(blank=True, max_length=150, null=True, verbose_name='crew pouring')),
                ('pdate', models.DateField(blank=True, null=True, verbose_name='pour date')),
                ('ctime', models.TimeField(blank=True, null=True, verbose_name='concrete time')),
                ('loads', models.FloatField(default=0, verbose_name='loads')),
                ('progress', models.CharField(choices=[('will call', 'will call'), ('scheduled', 'scheduled'), ('canceled', 'canceled'), ('in_progress', 'in_progress'), ('released', 'released'), ('complete', 'complete')], default='will call', max_length=11, verbose_name='pump progress')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('driver', models.ForeignKey(blank=True, db_constraint=False, limit_choices_to={'groups__name': 'Drivers'}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='delivery driver')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='orders.concreteorder', verbose_name='concrete order')),
            ],
            options={
                'verbose_name': 'historical pump',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='GravelDeliveryScheduleNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(max_length=250, verbose_name='Note')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='submitted by')),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gravel_delivery_notes', to='schedules.graveldeliveryschedule', verbose_name='pump')),
            ],
            options={
                'verbose_name': 'Gravel Delivery Note',
                'verbose_name_plural': 'Gravel Delivery Notes',
                'db_table': 'schedules_gravel_delivery_schedule_notes',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ConcreteOrderScheduleNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(max_length=250, verbose_name='Note')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='submitted by')),
                ('pump', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pump_schedule_notes', to='schedules.concreteorderschedule', verbose_name='pump')),
            ],
            options={
                'verbose_name': 'Pump Schedule Note',
                'verbose_name_plural': 'Pump Schedule Notes',
                'db_table': 'schedules_pump_schedule_notes',
                'managed': True,
            },
        ),
    ]
