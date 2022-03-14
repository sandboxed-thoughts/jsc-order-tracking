# Generated by Django 4.0.3 on 2022-03-09 20:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import localflavor.us.models
import phonenumber_field.modelfields
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StoneType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Stone Type')),
                ('description', models.TextField(blank=True, max_length=250, null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Stone Type',
                'verbose_name_plural': 'Stone Types',
                'db_table': 'stone_types',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(blank=True, max_length=50, null=True, verbose_name='Street Address')),
                ('city', models.CharField(blank=True, max_length=50, null=True, verbose_name='City')),
                ('state', localflavor.us.models.USStateField(blank=True, max_length=2, null=True, verbose_name='State')),
                ('zipcode', localflavor.us.models.USZipCodeField(blank=True, max_length=10, null=True, verbose_name='Zip')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Phone')),
                ('fax', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Fax')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Supplier Name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('website', models.URLField(blank=True, null=True, verbose_name='website')),
            ],
            options={
                'verbose_name': 'Supplier',
                'verbose_name_plural': 'Suppliers',
                'db_table': 'suppliers',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='HistoricalSupplier',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('street', models.CharField(blank=True, max_length=50, null=True, verbose_name='Street Address')),
                ('city', models.CharField(blank=True, max_length=50, null=True, verbose_name='City')),
                ('state', localflavor.us.models.USStateField(blank=True, max_length=2, null=True, verbose_name='State')),
                ('zipcode', localflavor.us.models.USZipCodeField(blank=True, max_length=10, null=True, verbose_name='Zip')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Phone')),
                ('fax', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Fax')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('name', models.CharField(db_index=True, max_length=50, verbose_name='Supplier Name')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('website', models.URLField(blank=True, null=True, verbose_name='website')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Supplier',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]