# Generated by Django 5.0.6 on 2024-06-15 22:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reports", "0009_alter_report_sections"),
    ]

    operations = [
        migrations.AddField(
            model_name="report",
            name="raw",
            field=models.TextField(default=None, null=True),
        ),
    ]