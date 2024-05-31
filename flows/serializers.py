from rest_framework import serializers
from flows import models


class FlowRunSerializer(serializers.Serializer):
    name = serializers.CharField()


class FlowResultInputSerializer(serializers.Serializer):
    prefect_id = serializers.CharField()
    flow_id = serializers.CharField()
    deployment_id = serializers.CharField()
    results = serializers.JSONField()


class FlowResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FlowResult
        fields = "__all__"
