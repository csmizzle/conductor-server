from django.db import models
from django.contrib.auth.models import User


class CrewTask(models.Model):
    """
    A task for a crew
    """

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    output = models.TextField()


class CrewRun(models.Model):
    """
    A crew run with tasks
    """

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    tasks = models.ManyToManyField(CrewTask, related_name="tasks")
    result = models.TextField()
