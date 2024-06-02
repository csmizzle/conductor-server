import uuid

from django.contrib.auth.models import User
from django.db import models


class TaskStatus(models.TextChoices):
    PENDING = "P", "Pending"
    RUNNING = "R", "Running"
    COMPLETED = "C", "Completed"
    FAILED = "F", "Failed"


class Task(models.Model):
    """
    Celery task model
    """

    task_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=2,
        choices=TaskStatus.choices,
        default=TaskStatus.PENDING,
    )


class URLSummary(models.Model):
    job_id = models.CharField(max_length=255)
    task_id = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="url_summary"
    )
    url = models.CharField(max_length=255)
    content = models.TextField()
    summary = models.TextField()
