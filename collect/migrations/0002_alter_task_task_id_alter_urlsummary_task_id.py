# Generated by Django 5.0.6 on 2024-05-12 19:20

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("collect", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="task_id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="urlsummary",
            name="task_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="url_summary",
                to="collect.task",
            ),
        ),
    ]
