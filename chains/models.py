import uuid
from django.contrib.auth.models import User
from django.db import models
from flows.models import Flow


class ChainEvent(models.Model):
    """
    Chain text event model
    """

    flow = models.ForeignKey(Flow, on_delete=models.CASCADE, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    chain_name = models.CharField(max_length=255)
    input = models.TextField(null=True, default=None)
    output = models.JSONField(null=True, default=None)


class ChainTaskStatus(models.TextChoices):
    PENDING = "P", "Pending"
    RUNNING = "R", "Running"
    COMPLETED = "C", "Completed"
    FAILED = "F", "Failed"


class ChainTask(models.Model):
    """
    Celery task model
    """

    event_id = models.ForeignKey(
        ChainEvent, on_delete=models.CASCADE, null=True, default=None
    )
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
