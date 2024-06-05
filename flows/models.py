from django.contrib.auth.models import User
from django.db import models


class FlowTrace(models.Model):
    """
    Flow trace object that contains the metadata of a flow run
    """

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    prefect_flow_id = models.CharField(max_length=255, null=True)
    prefect_deployment_id = models.CharField(max_length=255, null=True)
    prefect_name = models.CharField(max_length=255, null=True)
    prefect_parameters = models.JSONField(null=True)


class FlowResult(models.Model):
    """
    Store the results of a flow run
    """

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    flow_trace = models.ForeignKey(
        FlowTrace, on_delete=models.CASCADE, related_name="results"
    )
    results = models.JSONField()
