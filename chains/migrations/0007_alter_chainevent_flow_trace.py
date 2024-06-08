# Generated by Django 5.0.6 on 2024-06-08 14:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chains", "0006_rename_flow_chainevent_flow_trace"),
        ("flows", "0008_alter_flowresult_flow_trace"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chainevent",
            name="flow_trace",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="events",
                to="flows.flowtrace",
            ),
        ),
    ]
