# Generated by Django 4.0.3 on 2022-03-16 13:32

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import localflavor.us.models
import phonenumber_field.modelfields
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
        ('suppliers', '0001_initial'),
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConcreteOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_wall', models.BooleanField(default=True, verbose_name='is wall order')),
                ('is_footings', models.BooleanField(default=False, verbose_name='is footing order')),
                ('is_flatwork', models.BooleanField(default=False, verbose_name='is flatwork order')),
                ('po', models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator('[\\S\\w]')], verbose_name='purchase order')),
                ('etotal', models.SmallIntegerField(verbose_name='estimated total')),
                ('atotal', models.SmallIntegerField(blank=True, null=True, verbose_name='actual total')),
                ('qordered', models.SmallIntegerField(verbose_name='total ordered')),
                ('mix', models.CharField(choices=[('rich', 'rich'), ('standard', 'standard'), ('medium', 'medium'), ('lean', 'lean')], default='standard', max_length=10, verbose_name='mix')),
                ('slump', models.CharField(max_length=6, verbose_name='slump')),
                ('garage', models.CharField(blank=True, choices=[(None, None), ("4'", "4'"), ("8'", "8'"), ("9'", "9'")], default=None, max_length=3, null=True, verbose_name='garage size')),
                ('wea', models.CharField(blank=True, max_length=50, null=True, verbose_name='walkout egress area')),
                ('dispatcher', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='corders_accepted', to=settings.AUTH_USER_MODEL, verbose_name='dispatcher')),
            ],
            options={
                'verbose_name': 'concrete orders',
                'db_table': 'concrete_orders',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='FlatworkItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('description', models.TextField(verbose_name='item description')),
            ],
            options={
                'db_table': 'orders_concrete_flatwork_items',
            },
        ),
        migrations.CreateModel(
            name='InclimateWeather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp', models.CharField(max_length=50, verbose_name='temperature')),
                ('precip', models.CharField(max_length=50, verbose_name='precipitation')),
            ],
            options={
                'verbose_name': 'inclimate weather report',
                'verbose_name_plural': 'inclimate weather reports',
                'db_table': 'concrete_schedule_weather',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='InspectionAgency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(blank=True, max_length=50, null=True, verbose_name='Street Address')),
                ('city', models.CharField(blank=True, max_length=50, null=True, verbose_name='City')),
                ('state', localflavor.us.models.USStateField(blank=True, max_length=2, null=True, verbose_name='State')),
                ('zipcode', localflavor.us.models.USZipCodeField(blank=True, max_length=10, null=True, verbose_name='Zip')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Phone')),
                ('fax', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Fax')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='agency name')),
            ],
            options={
                'verbose_name': 'inspection agency',
                'verbose_name_plural': 'inspection agencies',
                'db_table': 'inspection_agency',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PumpSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crew', models.CharField(blank=True, max_length=150, null=True, verbose_name='crew pouring')),
                ('pdate', models.DateField(blank=True, null=True, verbose_name='pour date')),
                ('ctime', models.TimeField(blank=True, null=True, verbose_name='concrete time')),
                ('loads', models.FloatField(default=0, verbose_name='loads')),
                ('progress', models.CharField(choices=[('will call', 'will call'), ('scheduled', 'scheduled'), ('canceled', 'canceled'), ('in_progress', 'in_progress'), ('released', 'released'), ('complete', 'complete')], default='will call', max_length=11, verbose_name='pump progress')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='driver_pump_schedule', to=settings.AUTH_USER_MODEL, verbose_name='operator')),
                ('project_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pm_pump_schedule', to=settings.AUTH_USER_MODEL, verbose_name='project manager')),
            ],
            options={
                'verbose_name': 'pump schedule',
                'db_table': 'concrete_schedule',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='WeatherNotes',
            fields=[
                ('notemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.notemodel')),
                ('weather', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weather_notes', to='concrete.inclimateweather', verbose_name='weather note')),
            ],
            options={
                'verbose_name': 'note',
                'db_table': 'concrete_schedule_weather_notes',
                'managed': True,
            },
            bases=('core.notemodel',),
        ),
        migrations.CreateModel(
            name='ScheduleNotes',
            fields=[
                ('notemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.notemodel')),
                ('pump', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pump_notes', to='concrete.pumpschedule', verbose_name='pump scheduled')),
            ],
            options={
                'verbose_name': 'note',
                'verbose_name_plural': 'notes',
                'db_table': 'concrete_schedule_notes',
                'managed': True,
            },
            bases=('core.notemodel',),
        ),
        migrations.CreateModel(
            name='OrderNotes',
            fields=[
                ('notemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.notemodel')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='concrete.concreteorder', verbose_name='concrete order notes')),
            ],
            options={
                'verbose_name': 'order note',
                'verbose_name_plural': 'order notes',
                'db_table': 'orders_concrete_notes',
                'managed': True,
            },
            bases=('core.notemodel',),
        ),
        migrations.CreateModel(
            name='OrderInspection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itime', models.DateTimeField(verbose_name='inspection time')),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='concrete_inspection_orders', related_query_name='concrete_inspection_order', to='concrete.inspectionagency', verbose_name='inspection agency')),
                ('concrete_order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='concrete_inspection_agencys', related_query_name='concrete_inspection_agency', to='concrete.concreteorder', verbose_name='concrete order')),
            ],
            options={
                'verbose_name': 'concrete order inspection',
                'db_table': 'concrete_order_inspections',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='inclimateweather',
            name='pump',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='concrete.pumpschedule', verbose_name='inclimate weather'),
        ),
        migrations.CreateModel(
            name='HistoricalPumpSchedule',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('crew', models.CharField(blank=True, max_length=150, null=True, verbose_name='crew pouring')),
                ('pdate', models.DateField(blank=True, null=True, verbose_name='pour date')),
                ('ctime', models.TimeField(blank=True, null=True, verbose_name='concrete time')),
                ('loads', models.FloatField(default=0, verbose_name='loads')),
                ('progress', models.CharField(choices=[('will call', 'will call'), ('scheduled', 'scheduled'), ('canceled', 'canceled'), ('in_progress', 'in_progress'), ('released', 'released'), ('complete', 'complete')], default='will call', max_length=11, verbose_name='pump progress')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('driver', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='operator')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('project_manager', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='project manager')),
            ],
            options={
                'verbose_name': 'historical pump schedule',
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
                ('pump', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='concrete.pumpschedule', verbose_name='inclimate weather')),
            ],
            options={
                'verbose_name': 'historical inclimate weather report',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='FlatworkOrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concrete_order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='flatwork_items', related_query_name='order_item', to='concrete.concreteorder', verbose_name='concrete order')),
                ('flatwork_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_orders', related_query_name='item_order', to='concrete.flatworkitem', verbose_name='flatwork item')),
            ],
            options={
                'verbose_name': 'flatwork items',
                'db_table': 'concrete_order_flatwork_items',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ConcreteOrderLot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concrete_order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='concrete_orders', to='concrete.concreteorder', verbose_name='concrete order')),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pour_lots', to='clients.lot', verbose_name='lot')),
            ],
            options={
                'verbose_name': 'concrete order lot',
                'db_table': 'concrete_order_lots',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='concreteorder',
            name='items',
            field=models.ManyToManyField(through='concrete.FlatworkOrderItems', to='concrete.flatworkitem', verbose_name='items'),
        ),
        migrations.AddField(
            model_name='concreteorder',
            name='lots',
            field=models.ManyToManyField(related_name='orders', to='clients.lot', verbose_name='lots'),
        ),
        migrations.AddField(
            model_name='concreteorder',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='suppliers.supplier', verbose_name='supplier'),
        ),
    ]
