from django.db import models
from django.contrib.auth.models import User


class FlowResult(models.Model):
    """
    Store the results of a flow run
    """

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    context = models.JSONField()
    results = models.JSONField()
