# Generated by Django 5.0.6 on 2024-06-03 00:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chains", "0004_rename_content_chainevent_input"),
        ("flows", "0004_remove_flowresult_deployment_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="chainevent",
            name="flow",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="flows.flow",
            ),
        ),
        migrations.AddField(
            model_name="chaintask",
            name="event_id",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="chains.chainevent",
            ),
        ),
        migrations.AlterField(
            model_name="chainevent",
            name="input",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="chainevent",
            name="output",
            field=models.JSONField(default=None, null=True),
        ),
    ]