# Generated by Django 5.0.6 on 2024-06-22 22:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("agents", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="crewtask",
            name="agent_role",
            field=models.CharField(blank=True, max_length=510, null=True),
        ),
    ]