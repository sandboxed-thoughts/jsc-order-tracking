# Generated by Django 4.0.3 on 2022-03-26 16:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import localflavor.us.models
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(blank=True, max_length=50, null=True, verbose_name='City')),
                ('state', localflavor.us.models.USStateField(blank=True, max_length=2, null=True, verbose_name='State')),
                ('zipcode', localflavor.us.models.USZipCodeField(blank=True, max_length=10, null=True, verbose_name='Zip')),
                ('site_name', models.CharField(max_length=100, verbose_name='Site Name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('slug', models.SlugField(blank=True, verbose_name='url')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='last updated')),
                ('project_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pm_pump_schedules', to=settings.AUTH_USER_MODEL, verbose_name='project manager')),
            ],
            options={
                'verbose_name': 'Subdivision',
                'verbose_name_plural': 'Subdivisions',
                'db_table': 'sites_subdivisions',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='HistoricalSiteModel',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('city', models.CharField(blank=True, max_length=50, null=True, verbose_name='City')),
                ('state', localflavor.us.models.USStateField(blank=True, max_length=2, null=True, verbose_name='State')),
                ('zipcode', localflavor.us.models.USZipCodeField(blank=True, max_length=10, null=True, verbose_name='Zip')),
                ('site_name', models.CharField(max_length=100, verbose_name='Site Name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('slug', models.SlugField(blank=True, verbose_name='url')),
                ('created_on', models.DateTimeField(blank=True, editable=False, verbose_name='created on')),
                ('updated_on', models.DateTimeField(blank=True, editable=False, verbose_name='last updated')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('project_manager', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='project manager')),
            ],
            options={
                'verbose_name': 'historical Subdivision',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]