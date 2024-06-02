from django.contrib.auth.models import User
from django.db import models


class Flow(models.Model):
    """
    Flow object
    """

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    prefect_id = models.CharField(max_length=255, null=True)
    prefect_flow_id = models.CharField(max_length=255, null=True)
    prefect_deployment_id = models.CharField(max_length=255, null=True)


class FlowResult(models.Model):
    """
    Store the results of a flow run
    """

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    flow = models.ForeignKey(Flow, on_delete=models.CASCADE)
    results = models.JSONField()
