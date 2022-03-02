# Generated by Django 4.0.3 on 2022-03-02 20:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Concrete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otype', models.CharField(choices=[('walls', 'walls'), ('flatwork', 'flatwork'), ('footings', 'footings')], max_length=8, verbose_name='Pour Type')),
                ('pdate', models.DateField(blank=True, null=True, verbose_name='Pour Date')),
                ('incw', models.CharField(choices=[('rain', 'rain'), ('snow', 'snow'), ('none', 'none')], default='none', max_length=4, verbose_name='Inclimate Weather')),
                ('temp', models.CharField(choices=[('low', 'low'), ('high', 'high'), ('none', 'average')], default='none', max_length=4, verbose_name='Temperature')),
                ('bldr', models.CharField(max_length=50, verbose_name='Builder')),
                ('job_site', models.CharField(max_length=50, verbose_name='Job Site')),
                ('lot', models.CharField(help_text='separate each lot with a comma (,)', max_length=100, verbose_name='Lot Numbers')),
                ('item', models.CharField(max_length=50, verbose_name='Item')),
                ('cpour', models.CharField(blank=True, max_length=150, null=True, verbose_name='Crew Pouring')),
                ('supplier', models.CharField(max_length=50, verbose_name='Supplier')),
                ('dsph', models.CharField(max_length=50, verbose_name='Dispatcher')),
                ('ono', models.PositiveIntegerField(verbose_name='Order Number')),
                ('etot', models.PositiveIntegerField(verbose_name='Estimated Total')),
                ('qord', models.PositiveIntegerField(verbose_name='Quantity Ordered')),
                ('atot', models.PositiveIntegerField(blank=True, null=True, verbose_name='Actual Total')),
                ('ctype', models.CharField(choices=[('mix', 'mix'), ('slmp', 'slmp')], max_length=4, verbose_name='Mix/Slump')),
                ('pump', models.BooleanField(default=False, verbose_name='Pump')),
                ('pinfo', models.TextField(blank=True, max_length=150, null=True, verbose_name='Pump Info')),
                ('iagt', models.CharField(blank=True, max_length=50, null=True, verbose_name='Inspection Agency')),
                ('itime', models.DateTimeField(blank=True, null=True, verbose_name='Inspection Time')),
                ('ctime', models.DateTimeField(blank=True, null=True, verbose_name='Concrete Time')),
                ('pprog', models.CharField(choices=[('w/c', 'w/c'), ('cncl', 'cncl'), ('rlsd', 'rlsd'), ('complete', 'complete')], default='w/c', max_length=8, verbose_name='Pour Progress')),
                ('garage', models.PositiveSmallIntegerField(blank=True, help_text='only for footings', null=True, verbose_name='Garage Height (ft)')),
                ('wea', models.PositiveSmallIntegerField(blank=True, help_text='only for footings', null=True, verbose_name='Walkout Egress Area (ft)')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='order notes')),
            ],
            options={
                'verbose_name': 'Concrete Order',
                'verbose_name_plural': 'Concrete Orders',
                'db_table': 'c_orders',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Gravel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bldr', models.CharField(max_length=50, verbose_name='Builder')),
                ('job_site', models.CharField(max_length=50, verbose_name='Job Site')),
                ('lot', models.PositiveSmallIntegerField(verbose_name='Lot Number')),
                ('caller', models.CharField(max_length=50, verbose_name='Caller')),
                ('r_loads', models.PositiveIntegerField(verbose_name='Loads Requested')),
                ('d_loads', models.PositiveIntegerField(blank=True, null=True, verbose_name='Loads Delivered')),
                ('stone', models.CharField(max_length=50, verbose_name='Stone Type')),
                ('bsdt', models.CharField(choices=[('B', 'B/S'), ('D', 'D/T')], default='B', max_length=2, verbose_name='B/S D/T')),
                ('supplier', models.CharField(max_length=50, verbose_name='Supplier')),
                ('driver', models.CharField(blank=True, max_length=50, null=True, verbose_name='Driver')),
                ('n_date', models.DateField(verbose_name='Date Needed')),
                ('d_date', models.DateField(blank=True, null=True, verbose_name='Date Delivered')),
                ('priority', models.CharField(max_length=50, verbose_name='Priority')),
                ('po', models.PositiveIntegerField(verbose_name='P.O. Number')),
            ],
            options={
                'verbose_name': 'Gravel Order',
                'verbose_name_plural': 'Gravel Orders',
                'db_table': 'g_orders',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='HistoricalGravel',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('bldr', models.CharField(max_length=50, verbose_name='Builder')),
                ('job_site', models.CharField(max_length=50, verbose_name='Job Site')),
                ('lot', models.PositiveSmallIntegerField(verbose_name='Lot Number')),
                ('caller', models.CharField(max_length=50, verbose_name='Caller')),
                ('r_loads', models.PositiveIntegerField(verbose_name='Loads Requested')),
                ('d_loads', models.PositiveIntegerField(blank=True, null=True, verbose_name='Loads Delivered')),
                ('stone', models.CharField(max_length=50, verbose_name='Stone Type')),
                ('bsdt', models.CharField(choices=[('B', 'B/S'), ('D', 'D/T')], default='B', max_length=2, verbose_name='B/S D/T')),
                ('supplier', models.CharField(max_length=50, verbose_name='Supplier')),
                ('driver', models.CharField(blank=True, max_length=50, null=True, verbose_name='Driver')),
                ('n_date', models.DateField(verbose_name='Date Needed')),
                ('d_date', models.DateField(blank=True, null=True, verbose_name='Date Delivered')),
                ('priority', models.CharField(max_length=50, verbose_name='Priority')),
                ('po', models.PositiveIntegerField(verbose_name='P.O. Number')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Gravel Order',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalConcrete',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('otype', models.CharField(choices=[('walls', 'walls'), ('flatwork', 'flatwork'), ('footings', 'footings')], max_length=8, verbose_name='Pour Type')),
                ('pdate', models.DateField(blank=True, null=True, verbose_name='Pour Date')),
                ('incw', models.CharField(choices=[('rain', 'rain'), ('snow', 'snow'), ('none', 'none')], default='none', max_length=4, verbose_name='Inclimate Weather')),
                ('temp', models.CharField(choices=[('low', 'low'), ('high', 'high'), ('none', 'average')], default='none', max_length=4, verbose_name='Temperature')),
                ('bldr', models.CharField(max_length=50, verbose_name='Builder')),
                ('job_site', models.CharField(max_length=50, verbose_name='Job Site')),
                ('lot', models.CharField(help_text='separate each lot with a comma (,)', max_length=100, verbose_name='Lot Numbers')),
                ('item', models.CharField(max_length=50, verbose_name='Item')),
                ('cpour', models.CharField(blank=True, max_length=150, null=True, verbose_name='Crew Pouring')),
                ('supplier', models.CharField(max_length=50, verbose_name='Supplier')),
                ('dsph', models.CharField(max_length=50, verbose_name='Dispatcher')),
                ('ono', models.PositiveIntegerField(verbose_name='Order Number')),
                ('etot', models.PositiveIntegerField(verbose_name='Estimated Total')),
                ('qord', models.PositiveIntegerField(verbose_name='Quantity Ordered')),
                ('atot', models.PositiveIntegerField(blank=True, null=True, verbose_name='Actual Total')),
                ('ctype', models.CharField(choices=[('mix', 'mix'), ('slmp', 'slmp')], max_length=4, verbose_name='Mix/Slump')),
                ('pump', models.BooleanField(default=False, verbose_name='Pump')),
                ('pinfo', models.TextField(blank=True, max_length=150, null=True, verbose_name='Pump Info')),
                ('iagt', models.CharField(blank=True, max_length=50, null=True, verbose_name='Inspection Agency')),
                ('itime', models.DateTimeField(blank=True, null=True, verbose_name='Inspection Time')),
                ('ctime', models.DateTimeField(blank=True, null=True, verbose_name='Concrete Time')),
                ('pprog', models.CharField(choices=[('w/c', 'w/c'), ('cncl', 'cncl'), ('rlsd', 'rlsd'), ('complete', 'complete')], default='w/c', max_length=8, verbose_name='Pour Progress')),
                ('garage', models.PositiveSmallIntegerField(blank=True, help_text='only for footings', null=True, verbose_name='Garage Height (ft)')),
                ('wea', models.PositiveSmallIntegerField(blank=True, help_text='only for footings', null=True, verbose_name='Walkout Egress Area (ft)')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='order notes')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Concrete Order',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
