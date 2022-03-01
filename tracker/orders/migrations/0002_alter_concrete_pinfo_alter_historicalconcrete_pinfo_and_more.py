# Generated by Django 4.0.2 on 2022-02-28 21:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="concrete",
            name="pinfo",
            field=models.CharField(
                blank=True, max_length=150, null=True, verbose_name="Pump Info"
            ),
        ),
        migrations.AlterField(
            model_name="historicalconcrete",
            name="pinfo",
            field=models.CharField(
                blank=True, max_length=150, null=True, verbose_name="Pump Info"
            ),
        ),
        migrations.CreateModel(
            name="HistoricalConcreteNote",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                ("note", models.TextField(verbose_name="Note")),
                (
                    "created_on",
                    models.DateTimeField(
                        blank=True, editable=False, verbose_name="note added on"
                    ),
                ),
                (
                    "updated_on",
                    models.DateTimeField(
                        blank=True, editable=False, verbose_name="note last updated"
                    ),
                ),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField()),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="orders.concrete",
                        verbose_name="Order Note",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical Concrete Note",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": "history_date",
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="ConcreteNote",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("note", models.TextField(verbose_name="Note")),
                (
                    "created_on",
                    models.DateTimeField(auto_now=True, verbose_name="note added on"),
                ),
                (
                    "updated_on",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="note last updated"
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="c_order",
                        to="orders.concrete",
                        verbose_name="Order Note",
                    ),
                ),
            ],
            options={
                "verbose_name": "Concrete Note",
                "verbose_name_plural": "Concrete Notes",
                "db_table": "c_order_notes",
                "managed": True,
            },
        ),
    ]
