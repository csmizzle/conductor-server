from django.db import models


class AgentRun(models.Model):
    """Model for storing agent runs"""

    task = models.TextField()
    agent_name = models.CharField(max_length=100)
    output = models.TextField()

    def __str__(self):
        return f"Agent: {self.agent_name}\nTask: {self.task}\nOutput: {self.output}"
