from django.db import models
from django.contrib.auth.models import User
import uuid


class ChainTaskStatus(models.TextChoices):
    PENDING = "P", "Pending"
    RUNNING = "R", "Running"
    COMPLETED = "C", "Completed"
    FAILED = "F", "Failed"


class ChainTask(models.Model):
    """
    Celery task model
    """

    task_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=2,
        choices=ChainTaskStatus.choices,
        default=ChainTaskStatus.PENDING,
    )


class Summary(models.Model):
    task_id = models.ForeignKey(
        ChainTask, on_delete=models.CASCADE, related_name="summary"
    )

    content = models.TextField()
    summary = models.TextField()