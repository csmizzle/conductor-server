# Generated by Django 5.0.6 on 2024-06-04 01:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("flows", "0005_rename_flow_flowtrace_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="flowtrace",
            name="prefect_name",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="flowtrace",
            name="prefect_parameters",
            field=models.JSONField(null=True),
        ),
    ]
