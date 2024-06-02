from django.contrib.auth.models import User
from django.db import models


class FlowResult(models.Model):
    """
    Store the results of a flow run
    """

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    prefect_id = models.CharField(max_length=255, null=True)
    flow_id = models.CharField(max_length=255, null=True)
    deployment_id = models.CharField(max_length=255, null=True)
    results = models.JSONField()
