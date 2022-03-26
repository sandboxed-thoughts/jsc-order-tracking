# Generated by Django 4.0.3 on 2022-03-26 21:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_notemodel_options'),
        ('sites', '0002_alter_historicalsitemodel_project_manager_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteNote',
            fields=[
                ('notemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.notemodel')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.sitemodel', verbose_name='site note')),
            ],
            bases=('core.notemodel',),
        ),
    ]