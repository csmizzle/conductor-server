# Generated by Django 5.0.6 on 2024-06-08 15:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reports", "0003_remove_report_paragraphs_paragraph_report"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="paragraph",
            name="report",
        ),
        migrations.AddField(
            model_name="report",
            name="paragraphs",
            field=models.ManyToManyField(
                related_name="reports", to="reports.paragraph"
            ),
        ),
    ]