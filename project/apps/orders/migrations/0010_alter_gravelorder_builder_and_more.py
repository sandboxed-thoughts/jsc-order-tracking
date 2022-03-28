from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_alter_buildermodel_managers'),
        ('orders', '0009_remove_gravelorder_ddate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gravelorder',
            name='builder',
            field=models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.PROTECT, related_name='builder_gravel_orders', to='clients.buildermodel', verbose_name='builder'),
        ),
        migrations.AlterField(
            model_name='historicalgravelorder',
            name='builder',
            field=models.ForeignKey(blank=True, db_constraint=False, limit_choices_to={'is_active': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='clients.buildermodel', verbose_name='builder'),
        ),
    ]
