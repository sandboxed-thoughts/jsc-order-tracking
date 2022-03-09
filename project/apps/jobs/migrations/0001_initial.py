# Generated by Django 4.0.3 on 2022-03-09 20:58

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
            name='JobSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Site Name')),
                ('street', models.CharField(blank=True, max_length=50, null=True, verbose_name='Street Address')),
                ('city', models.CharField(blank=True, max_length=50, null=True, verbose_name='City')),
                ('state', localflavor.us.models.USStateField(blank=True, max_length=2, null=True, verbose_name='State')),
                ('zipcode', localflavor.us.models.USZipCodeField(blank=True, max_length=10, null=True, verbose_name='Zip')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'verbose_name': 'Job Site',
                'verbose_name_plural': 'Job Sites',
                'db_table': 'job_sites',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='HistoricalJobSite',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Site Name')),
                ('street', models.CharField(blank=True, max_length=50, null=True, verbose_name='Street Address')),
                ('city', models.CharField(blank=True, max_length=50, null=True, verbose_name='City')),
                ('state', localflavor.us.models.USStateField(blank=True, max_length=2, null=True, verbose_name='State')),
                ('zipcode', localflavor.us.models.USZipCodeField(blank=True, max_length=10, null=True, verbose_name='Zip')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Job Site',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
