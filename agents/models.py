from django.db import models


class AgentRun(models.Model):
    """Model for storing agent runs"""

    task = models.CharField(max_length=100)
    agent_name = models.CharField(max_length=100)
    output = models.CharField(max_length=5000)

    def __str__(self):
        return f"Agent: {self.agent_name}\nTask: {self.task}\nOutput: {self.output}"
