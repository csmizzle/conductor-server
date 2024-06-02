from django.db import models
from django.contrib.auth.models import User


class AgentRun(models.Model):
    """Model for storing agent runs"""

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.TextField()
    agent_name = models.CharField(max_length=100)
    output = models.TextField()

    def __str__(self):
        return f"Agent: {self.agent_name}\nTask: {self.task}\nOutput: {self.output}"
